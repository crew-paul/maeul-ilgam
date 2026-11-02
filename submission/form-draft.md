# Submission form — current English draft

Content aligned with the current implementation and fixed 1:52 demo on 2026-11-02. This is not a submitted entry. Confirm the team name/members, insert accessible video and site URLs, and answer surveys from actual experience.

- Team name: [confirm team name; suggested project name: Village Jobs]
- Track: Indie Developer Track
- Problem statement: Build for Your World
- Public GitHub Repository: https://github.com/crew-paul/maeul-ilgam
- 3-Minute Demo Video: [upload village-jobs-photo-story-fixed-en.mp4 and insert a judge-accessible URL]
- Live product: [public deployment pending; include URL in description and README when verified]
- Team members: Paul Hwang (studioKS) is shown in the supplied form; confirm every actual contributor.
- Most Viral X post: optional; leave empty unless entering with an actual qualifying post.

## Project Description

Village Jobs (마을일감) connects paid tasks from rural farmers with people nearby. It focuses on a practical situation: a farmer has produce to sell but needs help with product photography, packing or writing a product description, while a nearby young person may have the time and skills to help.

A farmer starts with a straightforward text form, with every field visible. Posting and viewing job details do not require sign-in. Meta can optionally extract the place, timing, pay and number of people needed from the request; the farmer reviews and edits the details before publishing. Applicants browse by town, verify a phone number or email, and explicitly consent to share their chosen contact with that farmer. The farmer can view applicants, edit or close a job, and arrange the work and payment directly. Withdrawing an application hides the contact from subsequent farmer requests; it cannot retract information already seen.

The app defaults to English and also supports Korean. Ten clearly labeled fictional sample tasks let judges explore the prototype. Data currently lives in a single server's memory and resets on restart. The recorded demo uses local test authentication, not real email delivery. The opening Korean farmer/youth photo story is AI-generated and fictional. We have not yet validated the app with older adults or measured employment, sales or population-retention outcomes.

Hackathon work shown in the repository and demo includes the text-first bilingual posting flow, Meta task extraction, review and publishing, anonymous posting ownership, task discovery, consent-based applications, contact visibility and withdrawal, and sample data. The video shows real browser-recorded app interactions after the illustrative photo story.

[Public app URL, after deployment and verification: ...]

## Describe your use of Meta products to build the submitted project

Meta Muse Spark 1.3, through Meta Model API, extracts structured task details from a written request: task description, location, timing, compensation and the number of people needed. The recorded demonstration includes an actual model response followed by human corrections and review. Unknown details remain available for the farmer to fill in; failed model calls show an error and retain the manual entry path.

The optional voice-entry path integrates Muse Voice Transcribe 1.0. Browser audio is converted to supported WAV and processed in memory rather than retained by the app. The submitted recording demonstrates text input; real microphone and rural-dialect performance have not been validated.

Muse Image 1.0 generated the eight fictional Korean character photographs used in the opening demo story. These are animated still photos with camera moves and dissolves, not generated live-action footage or real customer interviews. The product UI footage is an actual native browser recording. Runtime inference and the new generated visual assets use Meta models.

## Why are Meta's models important to your solution?

Farm work requests often begin as informal descriptions rather than completed forms. Muse Spark turns that description into editable task conditions, reducing repeated entry while keeping the farmer responsible for the final place, time and pay. Voice transcription provides an optional entry path for people who prefer speaking, while text entry remains the default and works without an AI call.

This integration connects model output to a complete posting and application workflow, rather than stopping at a generated answer. The farmer can inspect and correct the draft before publishing; applicants can see the actual conditions and choose whether to share their contact. We are evaluating Meta on these specific tasks and do not claim superiority over models we have not compared.

## Partner feedback, surveys and organizer permission

- Partner-technology feedback is optional. Mention Baseten, Modal or Fireworks only if actually used; no usage is established in the current submission record.
- Required Meta API likelihood/opinion answers and optional recommendation/comparison questions must reflect the participant's actual experience. They have not been selected on the participant's behalf.
- Review the permission for Meta/Cerebral Valley to use and promote submitted materials, and the official rules, before accepting. No consent checkbox or final submit action has been taken.
