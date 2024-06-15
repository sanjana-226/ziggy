import { Component, OnDestroy, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-drivers',
  templateUrl: './drivers.component.html',
  styleUrls: ['./drivers.component.css']
})
export class DriversComponent implements OnInit, OnDestroy {
  drivers: any;
  private updateSubscription: Subscription;

  constructor(private api: ApiService) {
    this.updateSubscription = interval(20000)
      .pipe(
        switchMap(() => this.api.getDrivers()) // Fetch drivers every second
      )
      .subscribe(
        data => {
          this.drivers = data;
          console.log('Updated drivers:', this.drivers);
        },
        error => {
          console.error('Error fetching drivers:', error);
        }
      );
  }
  ngOnInit(): void {
      this.api.getDrivers().subscribe(
        data => {
          this.drivers = data;
          console.log('Initial drivers:', this.drivers);
        },
        error => {
          console.error('Error fetching drivers:', error);
        }
      );

  }
  ngOnDestroy(): void {
    if (this.updateSubscription) {
      this.updateSubscription.unsubscribe();
    }
  }

  onRefresh(): void {
    this.api.getDrivers().subscribe(
      data => {
        this.drivers = data;
        console.log('Manual refresh - drivers:', this.drivers);
      },
      error => {
        console.error('Error fetching drivers:', error);
      }
    );
  }
}

