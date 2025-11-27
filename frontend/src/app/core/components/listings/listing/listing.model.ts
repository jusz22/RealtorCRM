export interface Listing {
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
}

export enum transactionType {
  sell = 'Sell',
  rent = 'Rent',
}

export enum propertyType {
  house = 'House',
  flat = 'Flat',
}
