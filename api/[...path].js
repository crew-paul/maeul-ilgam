import {openDatabase} from '../server/db.js';
import {createApp} from '../server/app.js';
import {seedDemoData} from '../server/demo-data.js';

// Each serverless instance owns its own disposable in-memory database.
// Never enable development authentication on a public deployment.
if (process.env.NODE_ENV === 'production' && process.env.AUTH_MODE === 'development') {
  throw new Error('Development authentication is forbidden in production');
}
if (process.env.VERCEL) process.env.TRUST_PROXY = '1';
const application = openDatabase().then(async db => {
  if (process.env.SEED_DEMO_DATA === '1') await seedDemoData(db);
  return createApp(db);
});
export default async function handler(req, res) {
  try {
    const app = await application;
    return app(req, res);
  } catch (error) {
    console.error('API initialization failed', error);
    res.statusCode = 503;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({error: {code: 'SERVICE_UNAVAILABLE'}}));
  }
}
