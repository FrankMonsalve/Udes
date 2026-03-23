import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AspiranteService } from '../../services/applicant';
import { Router, RouterModule } from '@angular/router';

/**
 * Componente para el formulario inicial de pre-inscripción
 */
@Component({
  selector: 'app-pre-registration',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './pre-registration.html',
})
export class PreRegistrationComponent implements OnInit {
  programas: any[] = [];
  datosFormulario: any = {
    tipo_documento: '',
    numero_documento: '',
    nombres: '',
    apellidos: '',
    genero: '',
    celular: '',
    correo: '',
    tipo_aspirante: '',
    programa_id: ''
  };

  constructor(
    private aspiranteService: AspiranteService, 
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  /**
   * Carga la lista de programas al inicializar el componente
   */
  ngOnInit() {
    this.aspiranteService.obtenerProgramas().subscribe({
      next: (res) => {
        this.programas = res;
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error al cargar programas', err)
    });
  }

  /**
   * Envía los datos de pre-registro al backend
   */
  enviarFormulario() {
    this.aspiranteService.preRegistro(this.datosFormulario).subscribe({
      next: () => {
        alert('¡Pre-registro exitoso! Ahora puede ingresar usando su número de documento como usuario y contraseña.');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Error en el registro', err);
        alert('Hubo un error al realizar el pre-registro. Por favor intente de nuevo.');
      }
    });
  }
}
