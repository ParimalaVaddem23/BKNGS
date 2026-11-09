# Requirements: BOOK-1 - Retrieve Booking Using Valid Booking ID

Generated: 2026-10-08 20:09:26

## Issue Details

| Field | Value |
|-------|-------|
| **Issue Key** | BOOK-1 |
| **Title** | Retrieve Booking Using Valid Booking ID |
| **Type** | Story |
| **Status** | To Do |
| **Assignee** | Parimala |
| **Story Points** | N/A |
| **Created** | 2026-09-06T11:02:58.699+0530 |
| **Jira Link** | [BOOK-1](https://parimalavaddem23.atlassian.net/browse/BOOK-1) |

## Description

{'type': 'doc', 'version': 1, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Objective:', 'marks': [{'type': 'strong'}]}, {'type': 'text', 'text': ' Verify that booking details are successfully returned for an existing booking.'}], 'attrs': {'localId': 'f999e3ff88af'}}, {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Steps:', 'marks': [{'type': 'strong'}]}], 'attrs': {'localId': '4ed74150ed5f'}}, {'type': 'orderedList', 'attrs': {'order': 1, 'localId': '3576c667dd37'}, 'content': [{'type': 'listItem', 'attrs': {'localId': 'fdd71da17c0b'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Send a GET request read the details from confluence page '}, {'type': 'inlineCard', 'attrs': {'url': 'https://parimalavaddem23.atlassian.net/wiki/spaces/BO/pages/14155970/Booking+APIs', 'localId': '9a567e82ce67'}}, {'type': 'text', 'text': ' '}], 'attrs': {'localId': 'e4d85b6bac0c'}}]}, {'type': 'listItem', 'attrs': {'localId': 'abb9ca79a54d'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Verify the response.'}], 'attrs': {'localId': 'b1a651fbf0e4'}}]}]}, {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Expected Result:', 'marks': [{'type': 'strong'}]}], 'attrs': {'localId': 'a01bd64dd902'}}, {'type': 'bulletList', 'content': [{'type': 'listItem', 'attrs': {'localId': '52491d80dfb5'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Status Code = '}, {'type': 'text', 'text': '200 OK', 'marks': [{'type': 'code'}]}], 'attrs': {'localId': '08a6393583db'}}]}, {'type': 'listItem', 'attrs': {'localId': '6f7495173c06'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Response contains:'}], 'attrs': {'localId': '35c7ea9c5f92'}}, {'type': 'bulletList', 'content': [{'type': 'listItem', 'attrs': {'localId': '5c7f16733aa8'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'firstname'}], 'attrs': {'localId': '99b3495f3657'}}]}, {'type': 'listItem', 'attrs': {'localId': '8fbd5d55f9ec'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'lastname'}], 'attrs': {'localId': '89b2e434090b'}}]}, {'type': 'listItem', 'attrs': {'localId': '09b2e372d94f'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'totalprice'}], 'attrs': {'localId': '0799d18fbfc6'}}]}, {'type': 'listItem', 'attrs': {'localId': '4853dd609227'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'depositpaid'}], 'attrs': {'localId': '30e45f19ce09'}}]}, {'type': 'listItem', 'attrs': {'localId': '4491debeaab5'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'bookingdates'}], 'attrs': {'localId': '6c694b74a99c'}}]}, {'type': 'listItem', 'attrs': {'localId': 'd47dac7d8fa6'}, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'additionalneeds'}], 'attrs': {'localId': 'ae45a913f886'}}]}], 'attrs': {'localId': '1add4cedc6bc'}}]}], 'attrs': {'localId': '929fe4ecfe3e'}}]}

## Acceptance Criteria

Objective: Verify that booking details are successfully returned for an existing booking.

Steps:

1. Send a GET request read the details from confluence page [Link: https://parimalavaddem23.atlassian.net/wiki/spaces/BO/pages/14155970/Booking+APIs]
2. Verify the response.

Expected Result:

• Status Code = 200 OK
• Response contains:• firstname
• lastname
• totalprice
• depositpaid
• bookingdates
• additionalneeds

## Labels

None

## Test Implementation Notes

### Key Scenarios
Based on the acceptance criteria above, the following test scenarios should be implemented:
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test scenario 3

### Dependencies & Preconditions
- List any dependencies here

### Edge Cases
- List any edge cases identified in the requirements

---

*This document was auto-generated from Jira issue BOOK-1 and linked Confluence pages.*
*Last updated: 2026-10-08 20:09:26*
