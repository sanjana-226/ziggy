import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: any[] = [];
  orderForm: any;

  constructor(private fb: FormBuilder, private api: ApiService) { }

  ngOnInit() {
    this.getOrders();
    console.log('init');
    console.log(this.orders);
    this.orderForm = this.fb.group({
      start_location: ['', Validators.required],
      end_location: ['', Validators.required]
    });
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
  onSubmit() {
    if (this.orderForm.valid) {
      console.log(this.orderForm.value);

      this.api.createOrder(this.orderForm.value).subscribe(
        (data) => {
          console.log('Order created successfully:', data);
          this.getOrders();
          this.orderForm.reset();
        },
        error => {
          console.error('Error creating order:', error);
        }
      );
    }
  }

  markAsDelivered(order: any) {
    console.log('markAsDelivered');
    console.log(order);
    this.api.updateOrder(order._id,).subscribe(data => {
      console.log(data);
      this.getOrders();
    }, error => {
      console.error('Error updating order:', error);
    });
  }


}
