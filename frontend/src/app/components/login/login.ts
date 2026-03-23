import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';
import { Router, RouterModule } from '@angular/router';

/**
 * Componente para el inicio de sesion de usuarios (Aspirantes y Administrativos)
 */
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.html',
})
export class LoginComponent {
  credenciales = { username: '', password: '' };

  constructor(private authService: AuthService, private router: Router) {}

  /**
   * Procesa el formulario de ingreso
   */
  iniciarSesion() {
    this.authService.login(this.credenciales).subscribe({
      next: (res) => {
        // Redireccionamos según el rol obtenido
        if (res.rol === 'ASP') {
          this.router.navigate(['/applicant-dashboard']);
        } else {
          this.router.navigate(['/admin-dashboard']);
        }
      },
      error: (err) => {
        console.error('Error de login', err);
        alert('Nombre de usuario o contraseña incorrectos.');
      }
    });
  }
}
