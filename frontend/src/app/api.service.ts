import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000';  

  constructor(private http: HttpClient) { }

  getOrders(): Observable<any> {
    return this.http.get<any[]>(`${this.baseUrl}/orders`);
  }

  // getOrderById(id: string): Observable<any> {
  //   return this.http.get(`${this.baseUrl}/orders/${id}`);
  // }

  createOrder(order: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/orders`, order);
  }

  updateOrder(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/orders/${id}`);
  }

  // Drivers API
  getDrivers(): Observable<any> {
    return this.http.get(`${this.baseUrl}/drivers`);
  }

  getDriverById(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/drivers/${id}`);
  }

  createDriver(driver: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/drivers`, driver);
  }

  updateDriver(id: string, driver: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/drivers/${id}`, driver);
  }

  deleteDriver(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/drivers/${id}`);
  }
}
