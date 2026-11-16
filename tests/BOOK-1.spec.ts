import { test, expect } from './fixtures';
import { BookingAPI } from './pom/BookingAPI';
import { CreateBookingRequest } from './interfaces/types';

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

test.describe('BOOK-1: Retrieve Booking by Valid ID', () => {
  test('should retrieve booking with all required fields', async ({ apiRequest, authToken }) => {
    const bookingAPI = new BookingAPI(apiRequest, authToken);

    // Arrange: create a booking so a valid ID exists
    const bookingPayload: CreateBookingRequest = {
      firstname: 'Jim',
      lastname: 'Brown',
      totalprice: 111,
      depositpaid: true,
      bookingdates: {
        checkin: '2025-01-01',
        checkout: '2025-01-05'
      },
      additionalneeds: 'Breakfast'
    };
    const createResponse = await bookingAPI.createBooking(bookingPayload);
    const bookingId = createResponse.bookingid;

    try {
      // Act: getBooking() throws on any non-200 status, so a resolved call proves AC2
      const getResponse = await bookingAPI.getBooking(bookingId);

      // Assert: presence and runtime types (AC3)
      expect(typeof getResponse.firstname, 'firstname should be a string').toBe('string');
      expect(getResponse.firstname.length, 'firstname should be non-empty').toBeGreaterThan(0);
      expect(typeof getResponse.lastname, 'lastname should be a string').toBe('string');
      expect(getResponse.lastname.length, 'lastname should be non-empty').toBeGreaterThan(0);
      expect(typeof getResponse.totalprice, 'totalprice should be a number').toBe('number');
      expect(getResponse.totalprice, 'totalprice should be >= 0').toBeGreaterThanOrEqual(0);
      expect(typeof getResponse.depositpaid, 'depositpaid should be a boolean').toBe('boolean');
      expect(getResponse.bookingdates, 'bookingdates should be present').toBeDefined();
      expect(getResponse.bookingdates.checkin, 'checkin should be an ISO 8601 date').toMatch(ISO_DATE);
      expect(getResponse.bookingdates.checkout, 'checkout should be an ISO 8601 date').toMatch(ISO_DATE);
      expect(typeof getResponse.additionalneeds, 'additionalneeds should be a string').toBe('string');

      // Assert: retrieved data matches the creation payload (AC4)
      expect(getResponse, 'retrieved booking should match the created booking').toEqual(bookingPayload);
    } finally {
      // Best-effort cleanup; must never fail the test
      try {
        await bookingAPI.deleteBooking(bookingId);
      } catch (error) {
        console.warn(`WARN: cleanup of booking ${bookingId} failed: ${(error as Error).message}`);
      }
    }
  });
});
