import { APIRequestContext } from '@playwright/test';
import { AuthRequest, AuthResponse } from '../interfaces/types';

export class AuthAPI {
  constructor(private apiRequest: APIRequestContext) {}

  /**
   * Creates and returns an auth token
   * @param credentials - AuthRequest with username and password
   * @returns Promise containing the auth token
   */
  async generateAuthToken(credentials: AuthRequest): Promise<string> {
    const response = await this.apiRequest.post('/auth', {
      data: credentials
    });

    if (response.status() !== 200) {
      throw new Error(`Failed to generate auth token. Status: ${response.status()}`);
    }

    const body: AuthResponse = await response.json();
    return body.token;
  }

  /**
   * Generates auth token with default credentials from environment variables
   * @returns Promise containing the auth token
   */
  async generateDefaultAuthToken(): Promise<string> {
    const username = process.env.AUTH_USERNAME;
    const password = process.env.AUTH_PASSWORD;

    if (!username || !password) {
      throw new Error('AUTH_USERNAME and AUTH_PASSWORD environment variables are not set');
    }

    return this.generateAuthToken({
      username,
      password
    });
  }
}
