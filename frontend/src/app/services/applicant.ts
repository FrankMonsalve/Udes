import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth';

/**
 * Servicio para gestionar las operaciones del Aspirante y administración
 * Se han eliminado los encabezados de seguridad (Sin JWT)
 */
@Injectable({
  providedIn: 'root'
})
export class AspiranteService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient, private authService: AuthService) { }

  /**
   * Obtiene la lista de programas académicos disponibles
   */
  obtenerProgramas(): Observable<any> {
    return this.http.get(`${this.apiUrl}/programas`);
  }

  /**
   * Realiza el pre-registro de un aspirante
   */
  preRegistro(datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/pre-registro`, datos);
  }

  /**
   * Obtiene la información del perfil del aspirante usando el ID de usuario guardado
   */
  obtenerPerfil(): Observable<any> {
    const usuario_id = this.authService.getUsuarioId();
    return this.http.get(`${this.apiUrl}/aspirante/perfil/${usuario_id}`);
  }

  /**
   * Actualiza los datos complementarios del aspirante
   */
  actualizarPerfil(datos: any): Observable<any> {
    const usuario_id = this.authService.getUsuarioId();
    return this.http.post(`${this.apiUrl}/aspirante/actualizar-perfil/${usuario_id}`, datos);
  }

  /**
   * Guarda la encuesta de mercadeo diligenciada
   */
  guardarEncuesta(datos: any): Observable<any> {
    const usuario_id = this.authService.getUsuarioId();
    return this.http.post(`${this.apiUrl}/aspirante/encuesta/${usuario_id}`, datos);
  }

  /**
   * Confirma la finalización del proceso de inscripción
   */
  confirmarInscripcion(): Observable<any> {
    const usuario_id = this.authService.getUsuarioId();
    return this.http.post(`${this.apiUrl}/aspirante/confirmar/${usuario_id}`, {});
  }

  /**
   * Lista todos los aspirantes (Sin restricciones por ahora)
   */
  obtenerAspirantes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/aspirantes`);
  }

  aprobarRYC(aspirante_id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/aprobar-ryc/${aspirante_id}`, {});
  }

  admitirCPG(aspirante_id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/admitir-cpg/${aspirante_id}`, {});
  }

  rechazarCPG(aspirante_id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/rechazar-cpg/${aspirante_id}`, {});
  }

  // Nuevos métodos para edición administrativa (MEI)
  obtenerPerfilPorId(usuario_id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/aspirante/perfil/${usuario_id}`);
  }

  actualizarPerfilPorId(usuario_id: number, datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/aspirante/actualizar-perfil/${usuario_id}`, datos);
  }

  confirmarInscripcionPorId(usuario_id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/aspirante/confirmar/${usuario_id}`, {});
  }
}
