Warning: True color (24-bit) support not detected. Using a terminal with true color enabled will result in a better visual experience.
YOLO mode is enabled. All tool calls will be automatically approved.
YOLO mode is enabled. All tool calls will be automatically approved.
Ripgrep is not available. Falling back to GrepTool.
Warning: Could not read directory D:\History vs Hype\.pytest_cache: EPERM: operation not permitted, scandir 'D:\History vs Hype\.pytest_cache'
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 6s.. Retrying after 7378ms...
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
    at Gaxios._request (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:8811:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:10774:16)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:272945:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:272743:23)
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:273597:19
    at async file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:250407:23
    at async retryWithBackoff (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:270684:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:293631:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/Benoi/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-7VVHSNDQ.js:293450:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'GeminiCLI-tui/0.42.0/gemini-2.5-flash (win32; x64; terminal) google-api-nodejs-client/9.15.1',
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
      date: 'Fri, 12 Jun 2026 12:46:27 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=737',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'f5ec021bdba58b80',
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
Attempt 1 failed: You have exhausted your capacity on this model. Your quota will reset after 0s.. Retrying after 5725ms...
## Johnny Harris, 'Why This Country Was Erased From History' (2024)

**(a) How the video opens (the hook framing, paraphrased)**
The video opens with a powerful, factual statement asserting that Kurds are arguably the largest stateless ethnic group globally. It highlights their shared culture, ethnicity, and language, contrasting this with their lack of self-determination. The hook immediately frames their situation as a consequence of being exploited as a geopolitical tool by global powers in the Middle East.

**(b) Hook type**
Cold_fact / Superlative Hook

**(c) 5 bullets on structure:**
*   Begins by defining the Kurds through their shared identity and their current stateless predicament, framing it as a geopolitical consequence.
*   Explores their historical presence in the Zagros Mountains, highlighting their centuries-long resistance and distinct cultural identity.
*   Discusses their significant autonomy under the Ottoman Empire, noting that "Kurdistan" was a recognized geographic region on European maps even without sovereign statehood.
*   Focuses heavily on the post-WWI period, specifically the broken promises of the Treaty of Sèvres (1920) and the subsequent division of Kurdish lands by the Treaty of Lausanne (1923).
*   Ends by illustrating the ongoing impact of these historical decisions on the Kurdish people, likely showing modern-day maps and conflicts related to their statelessness (inferred from common Johnny Harris narrative patterns).

**(d) What it claims about PRE-1916 Kurdish history, if anything**
The video claims that prior to 1916, Kurds had a centuries-long history in the Zagros Mountains, characterized by resistance to invaders and the maintenance of a distinct cultural identity. They were described as a nomadic people with a fluid sense of territory. Crucially, they maintained "large amounts of autonomy and freedom" under Ottoman rule, effectively functioning as a self-governing cultural entity, and "Kurdistan" was recognized as a geographic region on European maps, even if not as a sovereign state.

**(e) The title formula each uses and why it works for browse traffic**
Title: 'Why This Country Was Erased From History' (also commonly searched as 'Kurdistan - the State that Never Existed')
Formula: "Why [Dramatic Event/Absence] [Past Tense Action/State]" or "The [Entity] That [Contradictory State]"
Why it works:
*   **Intrigue & Mystery:** "Erased From History" creates immediate curiosity about *what* was erased and *why*.
*   **Emotional Resonance:** "Erased" implies injustice and a forgotten story, drawing viewers in emotionally.
*   **Contradiction:** "Country... Erased" or "State that Never Existed" presents a paradox that demands explanation.
*   **Educational Value:** Promises to answer a fundamental "why" question, appealing to viewers seeking knowledge.
*   **Strong Keywords:** "Country," "History," "State," "Kurdistan" are highly searchable terms related to geopolitics and forgotten histories.

## History Matters, 'Why Isn't There A Kurdistan? (Short Animated Documentary)' (2021)

**(a) How the video opens (the hook framing, paraphrased)**
The video opens with a generalized observation about groups living between powerful, often warring empires facing significant challenges. It then provides comparative examples like Poland and Korea, who, despite their historical struggles, eventually achieved statehood. This contrast sets up the Kurds as a unique case—a people caught between the Ottoman and Persian Empires who, unlike the others, have never achieved an internationally recognized nation, directly leading to the video's central question: "Why isn't there a Kurdistan?"

**(b) Hook type**
Contextual_opening / Question / Specificity_bomb (via comparative examples)

**(c) 5 bullets on structure:**
*   Starts with a broad historical generalization about imperial borderlands and then narrows down to specific comparative examples (Poland, Korea) before introducing the Kurdish situation as an exception.
*   Explains that prior to WWI, Kurdish territories were primarily divided between the Ottoman and Persian Empires, where a geopolitical stalemate maintained a stable but divided frontier.
*   Discusses the introduction of the "nation-state" concept by European advisors and its transformative impact on the region's political landscape.
*   Details how Ottoman centralization efforts, aimed at modernization and moving away from local autonomy, clashed significantly with traditional Kurdish self-governance and cultural identity.
*   Likely proceeds to cover the post-WWI period, focusing on key historical events like the Sykes-Picot Agreement and the subsequent failure to establish an independent Kurdistan, leading to the division of Kurdish lands among modern states (inferred from the video's core question and typical historical documentary structure).

**(d) What it claims about PRE-1916 Kurdish history, if anything**
The video explains that in the late 19th century, Kurds predominantly lived within the Ottoman and Persian Empires. It highlights that due to the persistent geopolitical stalemate between these two powers, Kurdish territory remained a relatively stable but divided frontier. The video also points out that the Ottoman government, influenced by the emerging "nation-state" concept, began stripping local Kurdish rulers of their traditional autonomy, moving towards a centralized administrative system that directly conflicted with Kurdish cultural identity and local governance structures.

**(e) The title formula each uses and why it works for browse traffic**
Title: 'Why Isn't There A Kurdistan? (Short Animated Documentary)'
Formula: "Why Isn't There A [Expected Entity/State]?" + "[Format/Style Descriptor]"
Why it works:
*   **Direct Question:** Poses a direct, thought-provoking question that taps into common geographical/historical curiosities.
*   **Problem-Solution Framing:** Implies that the video will provide a clear answer to a historical anomaly or injustice.
*   **Clear Topic:** "Kurdistan" unambiguously identifies the subject matter.
*   **Format Clarity:** "(Short Animated Documentary)" sets clear expectations for content, length, and style, appealing to viewers who prefer concise, visually engaging explanations.
*   **Searchability:** "Why Isn't There A Kurdistan" is a very natural and common search query for someone seeking information on this topic.

## Title lessons for a competing video

*   **Focus on the "Who" or "What If":** Both videos heavily focus on the "why" or "how" of Kurdish statelessness. A new video could explore the current *people* of Kurdistan (beyond just historical context) or a "what if" scenario about a recognized Kurdistan. For example, "The Kurds Today: A People Without Borders" or "What if Kurdistan Was a Nation?"
*   **Highlight the Future/Current Struggle/Resilience:** The existing titles are primarily past- and present-focused, often emphasizing the problem. A new title could emphasize the ongoing struggle, resilience, or future aspirations of the Kurdish people. For example, "The Unyielding Spirit of Kurdistan: A Fight for Recognition" or "Building Tomorrow: The Kurdish Quest for Statehood."
*   **Emphasize a Specific Angle/Region/Untold Story:** Instead of a broad overview, a competing video could focus on the Kurds in a particular country (e.g., "The Kurds of Syria: A Modern Alliance and Betrayal") or a specific aspect of their identity/culture that isn't solely tied to the "stateless" narrative, perhaps highlighting their unique language, music, or traditions.
*   **Contradiction/Irony with a different thematic twist:** While "erased from history" and "never existed" use contradiction effectively, another title could employ a different kind of irony, perhaps related to their geopolitical importance versus their lack of recognition, or their historical contributions versus current marginalization. For example, "The World's Most Important Non-Country: Kurdistan's Paradox."
*   **Solution-Oriented or Empowering Language:** Both existing titles inherently frame the situation as a problem or an absence. A competing video could use a title that suggests agency, resilience, or potential solutions/pathways forward, rather than just explaining the problem. For example, "The Path to Kurdistan: Can a Nation Be Born?" or "Beyond Borders: The Kurdish Dream of Self-Determination."
[ERROR] Invalid stream: The model returned an empty response or malformed tool call.
