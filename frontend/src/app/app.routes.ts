import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { PreRegistrationComponent } from './components/pre-registration/pre-registration';
import { ApplicantDashboardComponent } from './components/applicant-dashboard/applicant-dashboard';
import { AdminDashboardComponent } from './components/admin-dashboard/admin-dashboard';

export const routes: Routes = [
  { path: '', redirectTo: 'pre-registration', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'pre-registration', component: PreRegistrationComponent },
  { path: 'applicant-dashboard', component: ApplicantDashboardComponent },
  { path: 'admin-dashboard', component: AdminDashboardComponent },
];
