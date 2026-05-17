Warning: True color (24-bit) support not detected. Using a terminal with true color enabled will result in a better visual experience.
YOLO mode is enabled. All tool calls will be automatically approved.
YOLO mode is enabled. All tool calls will be automatically approved.
Ripgrep is not available. Falling back to GrepTool.
Warning: Could not read directory D:\History vs Hype\.pytest_cache: EPERM: operation not permitted, scandir 'D:\History vs Hype\.pytest_cache'
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:01:44 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=929',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '70e5c47cbdae518c',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:01:50 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=382',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'f92482692ff7b0fc',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:02:00 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=659',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '64f376d372e3668e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:02:39 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=512',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'a3aec39749ac708e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:02:44 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=475',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'ac70c8da7548a934',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:02:57 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=456',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '73f0c3a1bee3862e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 5s.. Retrying after 7138ms...
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:04:05 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=6385',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '7cf79d45e9907a66',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:04:13 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=512',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'f65885f729fbc589',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:04:26 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=601',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'b0f4c9f279f68080',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 4 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:04:42 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1095',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '25ddaf0c98b42e91',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 5 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:05:08 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=644',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '859338119d44ced9',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 6 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:05:36 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=583',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'c9c8bca82235a1e3',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 7 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:06:01 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=713',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e2ecccd0104870ff',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 8 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:06:40 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=484',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e77f15b5455999af',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 9 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:07:17 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=537',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e253c7ac4d054d68',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 2s.. Retrying after 5604ms...
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:08:47 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=616',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '2ee2185337c39aac',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:09:03 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=969',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '92c2c7128e7433e2',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:09:10 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1101',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '211b8a7dbbde053c',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:09:31 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=722',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '60cc52ee21305fd6',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-2.5-flash on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-2.5-flash on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-2.5-flash"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272793:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:272591:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:273444:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:250345:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:270539:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293199:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-NET4RIEQ.js:293037:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI/0.41.1/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.12.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-2.5-flash on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-2.5-flash"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '612',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 07 May 2026 14:09:39 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=941',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '64dd1cd14e343d30',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
All claims have been verified, and the findings have been compiled into `ModernClaimsVerification-Video52.md`.
