import { test as base, APIRequestContext } from '@playwright/test';
import { AuthResponse } from './interfaces/types';

export type TestFixtures = {
  apiRequest: APIRequestContext;
  authToken: string;
};

export const test = base.extend<TestFixtures>({
  apiRequest: async ({ request }, use) => {
    // apiRequest fixture provides the base request context
    await use(request);
  },

  authToken: async ({ apiRequest }, use) => {
    // Automatically generate auth token before each test using environment variables
    const username = process.env.AUTH_USERNAME;
    const password = process.env.AUTH_PASSWORD;

    if (!username || !password) {
      throw new Error('AUTH_USERNAME and AUTH_PASSWORD environment variables are not set');
    }

    const authResponse = await apiRequest.post('/auth', {
      data: {
        username,
        password
      }
    });

    if (authResponse.status() !== 200) {
      throw new Error('Failed to generate auth token');
    }

    const tokenBody: AuthResponse = await authResponse.json();
    const token = tokenBody.token;

    console.log('Auth token generated');

    // Use the token in tests
    await use(token);
  }
});

export { expect } from '@playwright/test';
