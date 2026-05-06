// Domain types mirroring the Odoo models

export type FarmerState = 'draft' | 'active' | 'suspended' | 'inactive';
export type PayoutMethod = 'bank' | 'mpesa' | 'cash';
export type QualityGrade = 'A' | 'B' | 'C' | 'rejected';
export type CollectionSession = 'morning' | 'evening';

export interface Farmer {
  id: number;
  farmer_code: string;
  name: string;
  id_number?: string;
  phone?: string;
  mpesa_number?: string;
  county?: string;
  cooperative_id?: [number, string] | false;
  collection_centre_id?: [number, string] | false;
  number_of_cows?: number;
  payout_method: PayoutMethod;
  state: FarmerState;
  total_collections?: number;
  total_payouts?: number;
  registration_date?: string;
}

export interface Cooperative {
  id: number;
  code: string;
  name: string;
  county?: string;
  phone?: string;
  farmer_count: number;
  centre_count: number;
  state: 'active' | 'inactive';
}

export interface CollectionRecord {
  id: number;
  name: string;
  collection_date: string;
  session: CollectionSession;
  farmer_id: [number, string];
  cooperative_id?: [number, string] | false;
  collection_centre_id?: [number, string] | false;
  quantity_litres: number;
  quality_grade: QualityGrade;
  unit_price: number;
  amount_due: number;
  state: string;
}

export interface QualityTest {
  id: number;
  name: string;
  test_date: string;
  session: CollectionSession;
  farmer_id?: [number, string] | false;
  fat_percentage?: number;
  snf_percentage?: number;
  acidity_ph?: number;
  antibiotics_present: boolean;
  grade: QualityGrade;
}

export interface PayoutBatch {
  id: number;
  name: string;
  period_start: string;
  period_end: string;
  cooperative_id?: [number, string] | false;
  payout_count: number;
  total_gross: number;
  total_deductions: number;
  total_net: number;
  state: 'draft' | 'computed' | 'approved' | 'disbursed' | 'cancelled';
}

export interface Payout {
  id: number;
  name: string;
  farmer_id: [number, string];
  period_start: string;
  period_end: string;
  total_litres: number;
  gross_amount: number;
  total_deductions: number;
  amount: number;
  payout_method: PayoutMethod;
  mpesa_number?: string;
  state: 'draft' | 'approved' | 'paid' | 'failed' | 'cancelled';
  payment_date?: string;
  transaction_reference?: string;
}

export interface MpesaTransaction {
  id: number;
  name: string;
  farmer_id?: [number, string] | false;
  phone_number: string;
  amount: number;
  mpesa_receipt_number?: string;
  state: 'pending' | 'queued' | 'success' | 'failed' | 'timeout';
  request_timestamp: string;
  result_description?: string;
}

export interface SmsMessage {
  id: number;
  name: string;
  farmer_id?: [number, string] | false;
  to_number: string;
  message_body: string;
  state: 'pending' | 'sent' | 'delivered' | 'failed';
  sent_at?: string;
}

export interface DashboardStats {
  totalFarmers: number;
  activeFarmers: number;
  todayCollections: number;
  todayLitres: number;
  pendingPayouts: number;
  pendingPayoutAmount: number;
  recentCollections: CollectionRecord[];
  pendingPayoutBatches: PayoutBatch[];
}
