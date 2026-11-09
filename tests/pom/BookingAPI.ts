import { APIRequestContext } from '@playwright/test';
import {
  CreateBookingRequest,
  CreateBookingResponse,
  GetBookingResponse,
  UpdateBookingRequest,
  UpdateBookingResponse,
  DeleteBookingResponse,
  PartialBookingInfo
} from '../interfaces/types';

export class BookingAPI {
  constructor(
    private apiRequest: APIRequestContext,
    private authToken?: string
  ) {}

  /**
   * Creates a new booking
   * @param bookingData - CreateBookingRequest with booking details
   * @returns Promise containing booking creation response
   */
  async createBooking(bookingData: CreateBookingRequest): Promise<CreateBookingResponse> {
    const response = await this.apiRequest.post('/booking', {
      data: bookingData
    });

    if (response.status() !== 200) {
      throw new Error(`Failed to create booking. Status: ${response.status()}`);
    }

    return response.json() as Promise<CreateBookingResponse>;
  }

  /**
   * Gets booking details by ID
   * @param bookingId - The booking ID to retrieve
   * @returns Promise containing booking details
   */
  async getBooking(bookingId: number): Promise<GetBookingResponse> {
    const response = await this.apiRequest.get(`/booking/${bookingId}`);

    if (response.status() !== 200) {
      throw new Error(`Failed to get booking. Status: ${response.status()}`);
    }

    return response.json() as Promise<GetBookingResponse>;
  }

  /**
   * Gets all booking IDs
   * @returns Promise containing array of booking info
   */
  async getAllBookings(): Promise<PartialBookingInfo[]> {
    const response = await this.apiRequest.get('/booking');

    if (response.status() !== 200) {
      throw new Error(`Failed to get all bookings. Status: ${response.status()}`);
    }

    return response.json() as Promise<PartialBookingInfo[]>;
  }

  /**
   * Updates an existing booking
   * @param bookingId - The booking ID to update
   * @param bookingData - UpdateBookingRequest with updated booking details
   * @returns Promise containing updated booking response
   */
  async updateBooking(
    bookingId: number,
    bookingData: UpdateBookingRequest
  ): Promise<UpdateBookingResponse> {
    if (!this.authToken) {
      throw new Error('Auth token is required for updating bookings');
    }

    const response = await this.apiRequest.put(`/booking/${bookingId}`, {
      headers: {
        Cookie: `token=${this.authToken}`
      },
      data: bookingData
    });

    if (response.status() !== 200) {
      throw new Error(`Failed to update booking. Status: ${response.status()}`);
    }

    return response.json() as Promise<UpdateBookingResponse>;
  }

  /**
   * Deletes a booking
   * @param bookingId - The booking ID to delete
   * @returns Promise containing delete response
   */
  async deleteBooking(bookingId: number): Promise<DeleteBookingResponse> {
    if (!this.authToken) {
      throw new Error('Auth token is required for deleting bookings');
    }

    const response = await this.apiRequest.delete(`/booking/${bookingId}`, {
      headers: {
        Cookie: `token=${this.authToken}`
      }
    });

    if (response.status() !== 201) {
      throw new Error(`Failed to delete booking. Status: ${response.status()}`);
    }

    return {
      status: response.status(),
      statusText: response.statusText()
    } as DeleteBookingResponse;
  }

  /**
   * Partially updates a booking (PATCH)
   * @param bookingId - The booking ID to update
   * @param partialData - Partial booking data to update
   * @returns Promise containing updated booking response
   */
  async partialUpdateBooking(
    bookingId: number,
    partialData: Partial<UpdateBookingRequest>
  ): Promise<UpdateBookingResponse> {
    if (!this.authToken) {
      throw new Error('Auth token is required for updating bookings');
    }

    const response = await this.apiRequest.patch(`/booking/${bookingId}`, {
      headers: {
        Cookie: `token=${this.authToken}`
      },
      data: partialData
    });

    if (response.status() !== 200) {
      throw new Error(`Failed to partially update booking. Status: ${response.status()}`);
    }

    return response.json() as Promise<UpdateBookingResponse>;
  }

  /**
   * Sets the auth token for authenticated operations
   * @param token - The auth token
   */
  setAuthToken(token: string): void {
    this.authToken = token;
  }
}
