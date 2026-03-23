import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

/**
 * Servicio encargado de la autenticación de usuarios
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  /**
   * Realiza el proceso de inicio de sesión (Sin JWT)
   */
  login(credenciales: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credenciales).pipe(
      tap((res: any) => {
        // Almacenamos el rol y el ID de usuario localmente
        localStorage.setItem('rol', res.rol);
        localStorage.setItem('usuario_id', res.usuario_id.toString());
      })
    );
  }

  logout() {
    localStorage.removeItem('rol');
    localStorage.removeItem('usuario_id');
  }

  getRol() {
    return localStorage.getItem('rol');
  }

  getUsuarioId() {
    return localStorage.getItem('usuario_id');
  }
}
