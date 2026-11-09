// Request Interfaces
export interface AuthRequest {
  username: string;
  password: string;
}

export interface BookingDates {
  checkin: string;
  checkout: string;
}

export interface CreateBookingRequest {
  firstname: string;
  lastname: string;
  totalprice: number;
  depositpaid: boolean;
  bookingdates: BookingDates;
  additionalneeds?: string;
}

export interface UpdateBookingRequest {
  firstname: string;
  lastname: string;
  totalprice: number;
  depositpaid: boolean;
  bookingdates: BookingDates;
  additionalneeds?: string;
}

export interface DeleteBookingRequest {
  bookingid: number;
}

// Response Interfaces
export interface AuthResponse {
  token: string;
}

export interface BookingData {
  firstname: string;
  lastname: string;
  totalprice: number;
  depositpaid: boolean;
  bookingdates: BookingDates;
  additionalneeds?: string;
}

export interface CreateBookingResponse {
  bookingid: number;
  booking: BookingData;
}

export interface GetBookingResponse extends BookingData {}

export interface UpdateBookingResponse extends BookingData {}

export interface DeleteBookingResponse {
  status: number;
  statusText: string;
}

export interface PartialBookingInfo {
  bookingid: number;
  url: string;
}
