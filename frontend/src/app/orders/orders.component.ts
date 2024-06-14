import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent {
  orders: any;
  constructor(private api: ApiService) { }
  

  getOrders() {
    this.orders = this.api.getOrders();
    console.log(this.orders);
    // get orders from the eve backend

  }
}
