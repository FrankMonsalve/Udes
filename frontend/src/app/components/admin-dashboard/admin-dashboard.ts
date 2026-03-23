import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AspiranteService } from '../../services/applicant';
import { AuthService } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.html',
})
export class AdminDashboardComponent implements OnInit {
  aspirantes: any[] = [];
  rol: string | null = '';
  programas: any[] = [];
  
  // Estado para la edición de MEI
  editandoAspirante: any = null;
  // Estado para la visualización (ojo)
  aspiranteSeleccionado: any = null;

  constructor(
    private aspiranteService: AspiranteService, 
    private authService: AuthService, 
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.rol = this.authService.getRol();
    this.cargarAspirantes();
    this.aspiranteService.obtenerProgramas().subscribe(res => {
      this.programas = res;
    });
  }

  cargarAspirantes() {
    this.aspiranteService.obtenerAspirantes().subscribe({
      next: (res) => {
        this.aspirantes = [...res];
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error al cargar aspirantes', err);
        this.router.navigate(['/login']);
      }
    });
  }

  // Lógica de edición para MEI
  iniciarEdicion(aspirante: any) {
    // Primero limpiamos cualquier estado previo
    this.editandoAspirante = null;
    this.cdr.detectChanges();

    // Obtenemos el perfil completo para editar usando el usuario_id del objeto aspirante de la lista
    this.aspiranteService.obtenerPerfilPorId(aspirante.usuario_id).subscribe({
      next: (res) => {
        console.log('Datos recibidos para edición:', res);
        this.editandoAspirante = { ...res };
        
        // Asegurar que programa_id sea tratado como número para el select
        if (this.editandoAspirante.programa_id !== undefined && this.editandoAspirante.programa_id !== null) {
          this.editandoAspirante.programa_id = Number(this.editandoAspirante.programa_id);
        }
        
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error al cargar perfil para edición', err)
    });
  }

  cancelarEdicion() {
    this.editandoAspirante = null;
  }

  // Lógica para ver información (readonly)
  verDetalles(aspirante: any) {
    this.aspiranteService.obtenerPerfilPorId(aspirante.usuario_id).subscribe({
      next: (res) => {
        this.aspiranteSeleccionado = { ...res };
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error al cargar detalles', err)
    });
  }

  cerrarDetalles() {
    this.aspiranteSeleccionado = null;
  }

  guardarCambiosMEI() {
    this.aspiranteService.actualizarPerfilPorId(this.editandoAspirante.usuario_id, this.editandoAspirante).subscribe(() => {
      // Según requerimiento, MEI "finaliza la inscripción nuevamente"
      this.aspiranteService.confirmarInscripcionPorId(this.editandoAspirante.usuario_id).subscribe(() => {
        alert('Información corregida y suscripción finalizada exitosamente.');
        this.editandoAspirante = null;
        this.cargarAspirantes();
      });
    });
  }

  // Acciones de RYC y CPG
  aprobarRegistro(aspiranteId: number) {
    if (confirm('¿Está seguro de aprobar esta inscripción?')) {
      this.aspiranteService.aprobarRYC(aspiranteId).subscribe(() => {
        alert('Inscripción aprobada');
        this.cargarAspirantes();
      });
    }
  }

  admitirAspirante(aspiranteId: number) {
    if (confirm('¿Está seguro de admitir a este aspirante?')) {
      this.aspiranteService.admitirCPG(aspiranteId).subscribe(() => {
        alert('Aspirante admitido');
        this.cargarAspirantes();
      });
    }
  }

  rechazarAspirante(aspiranteId: number) {
    if (confirm('¿Está seguro de rechazar esta inscripción?')) {
      this.aspiranteService.rechazarCPG(aspiranteId).subscribe(() => {
        alert('Inscripción rechazada');
        this.cargarAspirantes();
      });
    }
  }

  cerrarSesion() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
