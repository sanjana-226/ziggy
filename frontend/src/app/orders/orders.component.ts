import { Component, OnDestroy, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { FormBuilder, Validators } from '@angular/forms';
import { ValidatorFn, AbstractControl } from '@angular/forms';
import { Subscription, interval, switchMap } from 'rxjs';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit, OnDestroy {
  orders: any[] = [];
  orderForm: any;
  private updateSubscription: Subscription = new Subscription;

  constructor(private fb: FormBuilder, private api: ApiService) { }

  ngOnInit(): void {
    this.getOrders();
    this.orderForm = this.fb.group({
      start_location: ['', [Validators.required, Validators.minLength(2), coordinateFormatValidator()]],
      end_location: ['', [Validators.required, Validators.minLength(2), coordinateFormatValidator()]],
    });

    this.updateSubscription = interval(20000)
      .pipe(
        switchMap(() => this.api.getOrders())
      )
      .subscribe(
        data => {
          this.orders = data;
          console.log('Updated orders:', this.orders);
        },
        error => {
          console.error('Error fetching orders:', error);
        }
      );
  }

  ngOnDestroy(): void {
    if (this.updateSubscription) {
      this.updateSubscription.unsubscribe();
    }
  }

  onRefresh(): void {
    this.getOrders();
  }

  getOrders(): void {
    this.api.getOrders().subscribe(
      data => {
        this.orders = data;
        console.log('Initial orders:', this.orders);
      },
      error => {
        console.error('Error fetching orders:', error);
      }
    );
  }

  onSubmit(): void {
    if (this.orderForm.valid) {
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

  markAsDelivered(order: any): void {
    this.api.doneOrder(order._id).subscribe(
      data => {
        console.log('Order marked as delivered:', data);
        this.getOrders();
      },
      error => {
        console.error('Error updating order:', error);
      }
    );
  }
}

function coordinateFormatValidator(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } | null => {
      const valid = /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/.test(control.value);
      return valid ? null : { invalidFormat: { value: control.value } };
  };
}