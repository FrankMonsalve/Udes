import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AspiranteService } from '../../services/applicant';
import { Router } from '@angular/router';

/**
 * Panel de control para el Aspirante
 * Gestiona el diligenciamiento paso a paso de la inscripción
 */
@Component({
  selector: 'app-applicant-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './applicant-dashboard.html',
})
export class ApplicantDashboardComponent implements OnInit {
  aspirante: any = {};
  pestanaActiva = 1;

  constructor(private aspiranteService: AspiranteService, private router: Router) {}

  /**
   * Carga la información del perfil al iniciar
   */
  ngOnInit() {
    this.aspiranteService.obtenerPerfil().subscribe({
      next: (res) => {
        this.aspirante = res;
      },
      error: (err) => {
        console.error('Error al cargar perfil', err);
        this.router.navigate(['/login']);
      }
    });
  }

  /**
   * Guarda los datos complementarios del Tab 1
   */
  guardarPerfil() {
    this.aspiranteService.actualizarPerfil(this.aspirante).subscribe({
      next: () => {
        alert('Datos complementarios guardados exitosamente.');
        this.pestanaActiva = 2; // Avanza automáticamente a documentos
      },
      error: (err) => alert('Error al guardar datos.')
    });
  }

  /**
   * Avanza manualmente a la siguiente pestana
   */
  siguientePestana() {
    this.pestanaActiva++;
  }

  /**
   * Guarda la encuesta de mercadeo del Tab 3
   */
  guardarEncuesta() {
    this.aspiranteService.guardarEncuesta(this.aspirante).subscribe({
      next: () => {
        alert('Encuesta guardada exitosamente.');
        this.pestanaActiva = 4; // Avanza a confirmación
      },
      error: (err) => alert('Error al guardar encuesta.')
    });
  }

  /**
   * Finaliza formalmente el proceso de inscripción
   */
  finalizarInscripcion() {
    this.aspiranteService.confirmarInscripcion().subscribe({
      next: () => {
        alert('¡Inscripción finalizada con éxito!');
        this.ngOnInit(); // Refresca para actualizar el estado en pantalla
      },
      error: (err) => alert('Error al confirmar inscripción.')
    });
  }
}
