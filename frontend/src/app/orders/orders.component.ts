import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: any[] = [];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.getOrders();
    console.log('init');
    console.log(this.orders);
  }

  onRefresh() {
    this.getOrders();
    console.log('refresh');
    console.log(this.orders);
  }

  ngAfterViewInit() {
    this.getOrders();
    console.log('init');
    console.log(this.orders);
  }

  getOrders() {
    this.api.getOrders().subscribe(data => {
      this.orders = data;
      console.log(this.orders);
    }, error => {
      console.error('Error fetching orders:', error);
    });
  }

  

markAsDelivered(order: any) {
  console.log('markAsDelivered');
  console.log(order);
    this.api.updateOrder(order._id, ).subscribe(data => {
        console.log(data);
        this.getOrders();
    }, error => {
        console.error('Error updating order:', error);
    });
}

}
