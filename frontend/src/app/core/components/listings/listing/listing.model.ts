export interface Listing extends ListingInput {
  price_per_area: number;
  id: string;
  created_at: Date;
}

export interface ListingInput {
  client_id: string;
  title: string;
  location: string;
  street: string;
  price: number;
  area: number;
  property_type: propertyType;
  description: string;
  transaction_type: transactionType;
  floor: string;
  num_of_floors: string;
  build_year: string;
  status: status;
  user_id?: number;
}

export enum transactionType {
  sell = 'Sell',
  rent = 'Rent',
}

export enum propertyType {
  house = 'House',
  apartment = 'Apartment',
}

export enum status {
  available = 'Available',
  pending = 'Pending',
  closed = 'Closed',
}
