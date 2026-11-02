import { test } from 'node:test';
import assert from 'node:assert/strict';
import { extractDraft } from './logic.js';
test('demo draft does not invent unknown terms', () => { assert.deepEqual(extractDraft('Need help taking photos'), { task:'Need help taking photos', location:'', timing:'', compensation:'' }); });
