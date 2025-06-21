export interface Message {
  userId: string;
  role: string;
  text: string;
  ts: string;
}

export interface User {
  id: string;
  name: string;
  role: string;
}