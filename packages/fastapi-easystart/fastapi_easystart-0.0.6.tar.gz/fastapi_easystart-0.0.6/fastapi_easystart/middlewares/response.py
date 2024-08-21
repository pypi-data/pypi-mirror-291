import json

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi_easystart.schemas.response import APIBaseResponse

RESPONSE_STATUS_CODE = [200, 201, 202]


class CustomBaseHTTPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response_data = await call_next(request)
        status_code = response_data.status_code
        # Ensure we have the request_id from response headers
        request_id = request.state.request_id if hasattr(request.state, 'request_id') else None
        if request_id is None:
            request_id = response_data.headers.get('x-request-id')

        try:
            # getting content
            is_binary_content, body_content = await self.extract_results(response_data)

            # Return the original response for binary content or HTML
            if is_binary_content or response_data.media_type == "text/html":
                # do something with body ...
                return Response(
                    content=body_content,
                    status_code=response_data.status_code,
                    headers=dict(response_data.headers),
                    media_type=response_data.media_type
                )

            # Determine the type of content and structure the results accordingly
            response_content = APIBaseResponse.get_structure_results(status_code, request_id, body_content)

            # Copy headers from response_data, excluding Content-Length
            response_headers = dict(response_data.headers)
            # Remove the old content-length header if present
            response_headers.pop('content-length', None)
            return Response(content=response_content, media_type="application/json",
                            status_code=response_data.status_code, headers=response_headers)

        except Exception as e:
            # Handle validation errors here and return a consistent response
            error_response = APIBaseResponse.get_structure_results(
                status_code=501,
                request_id=request_id,
                content={
                    "message": "Oops! An unresolved exceptions occurred.",
                    "detail": str(e),
                }
            )
            response = JSONResponse(content=error_response, status_code=501)
            # Copy headers from response_data, excluding Content-Length
            response_headers = dict(response_data.headers)
            # Remove the content-length header if present
            response_headers.pop('content-length', None)
            response.headers.update(response_headers)
            return response

    async def extract_results(self, response_data: Response):
        if response_data.media_type == "application/json":
            content = await response_data.json()
            return False, content.get("results", {})
        elif response_data.media_type == "text/plain":
            return False, {"text_content": response_data.content.decode("utf-8")}
        elif isinstance(response_data, StreamingResponse):
            # Use body_iterator to gather content from streaming response
            # body = b""
            # async for chunk in response.body_iterator:
            #     body += chunk
            chunks = [chunk async for chunk in response_data.body_iterator]
            response_content = b''.join(chunks)
            try:
                # Attempt to detect JSON content
                json_content = json.loads(response_content.decode("utf-8"))
                return False, json_content
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Not JSON or No content type found or unrecognized, treat as binary
                return True, response_content
        else:
            # Handle other content types
            return True, response_data
