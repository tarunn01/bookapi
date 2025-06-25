✅ 1xx – Informational
100 Continue – Request received, continue sending.

101 Switching Protocols – Server switching protocols (WebSocket, etc.).



✅ 2xx – Success
200 OK – Standard success response.

201 Created – Resource created (e.g., after POST).

204 No Content – Success, but no data to return.

✅ 3xx – Redirection
301 Moved Permanently – Resource permanently moved.

302 Found – Temporary redirect.

304 Not Modified – Cached content is still valid.


✅ 4xx – Client Errors
400 Bad Request – Invalid request data.

401 Unauthorized – Missing or bad auth.

403 Forbidden – Authenticated but not allowed.

404 Not Found – Resource doesn't exist.

405 Method Not Allowed – HTTP method not allowed.

409 Conflict – Duplicate or conflicting data.

422 Unprocessable Entity – Validation failed.




✅ 5xx – Server Errors
500 Internal Server Error – Unexpected crash or bug.

502 Bad Gateway – Invalid response from upstream server.

503 Service Unavailable – Server down or overloaded.