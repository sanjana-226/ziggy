import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrdersComponent } from './orders/orders.component';
import { HomeComponent } from './home/home.component';
import { DriversComponent } from './drivers/drivers.component';


const routes: Routes = [
  {path:'',component:HomeComponent},
  { path: 'orders', component: OrdersComponent },
  { path: 'drivers', component: DriversComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
