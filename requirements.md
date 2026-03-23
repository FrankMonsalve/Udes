La Universidad de Santander UDES está interesada en contratar el desarrollo de una aplicación WEB para automatizar el **proceso de inscripciones de aspirantes a programas de pregrado.**

Existen los siguientes roles de usuario:

- Usuario Aspirante (**ASP**) => Se postula para estudiar un programa académico.
- Usuario Registro y Control (**RYC**) => Revisa, aprueba o hace observaciones de las inscripciones.
- Usuario Mercadeo Institucional (**MEI**) => Revisa, edita o corrige información registrada por los aspirantes.
- Usuario Coordinador de Programa (**CPG**) => Revisa, admite o rechaza inscripciones de aspirantes.

El proceso es el siguiente:

El aspirante ingresa al sitio web de inscripciones donde realiza un registro de pre-inscripción con sus datos básicos (tipo documento, número documento, nombres, apellidos, genero, celular, correo), programa al que aspira y tipo de aspirante (nuevo nacional, nuevo internacional, transferencia interna entre programas, transferencia externa otras universidades).

Una vez realizada la pre-inscripción los usuarios de RYC, MEI y CPG son notificados por correo electrónico de la nueva inscripción. El usuario ASP recibe un correo con la URL y credenciales (cedula y contraseña) para continuar diligenciando información de la inscripción.

EL usuario ASP ingresa con las credenciales al sitio web y en el primer tab diligencia un formulario con los datos complementarios (fecha de nacimiento, lugar de nacimiento, dirección de residencia, estrato). En el segundo tab hace la carga de la foto (JPG), documento de identidad (PDF), diploma de bachiller (PDF). En el tercer tab diligencia una breve encuesta de mercadeo con 3 preguntas: 1) Motivación para estudiar en la Universidad: _\[pregunta abierta\]_; 2) Medio por el cual se enteró de la Institución: _\[Visita al colegio o la Institución, Recomendación; Funcionario institución\]_; 3) Canal informativo por el cual se enteró de la institución: _\[Internet, Radio, Redes sociales, Televisión\]_. Por último el usuario ASP confirma la inscripción mediante un botón que valida que haya introducido todos los datos requeridos.

Una vez finalizada la inscripción el usuario de RYC valida los datos y la carga de documentos, **aprobando** la inscripción o realizando alguna **observación** o corrección. En ambos casos debe notificar por correo al ASP.

El usuario de MEI revisa la información registrada por el ASP y puede editar o corregir información del ASP o cargar documentos y finalizar la inscripción nuevamente.

El usuario CPG recibe una notificación por correo cuando el usuario de RYC aprueba la inscripción y revisa la información consignada por el aspirante, luego de lo cual toma la decisión de Aprobar o Rechazar la inscripción del aspirante. En ambos casos se notifica por correo al ASP.

En la vista de aspirantes los usuarios RYC, MEI y CPG podrán ver la lista de aspirantes inscritos y su estado el cual puede ser:

- PRE-INSCRIPCION: El aspirante realizó el registro de pre-inscripción pero no ha ingresado con las credenciales para continuar con el proceso de inscripción.
- DILIGENCIANDO FORMULARIO: El aspirante ya ingreso con las credenciales para continuar con la inscripción.
- FINALIZO INSCRIPCION: El aspirante ya finalizó y confirmó la inscripción.
- APROBADO: El usuario de RYC ya aprobó la inscripción
- ADMITIDO: El usuario CPG admitió al aspirante.
- RECHAZADO: El usuario CPG rechazó al aspirante.

Desde la misma vista dependiendo del rol del usuario (RYC, MEI y CPG) se podrá gestionar la inscripción de los aspirantes.

Para la sustentación se debe contar con la siguiente información:

\* Un usuario de RYC

\* Un usuario de MEI

\* Un usuario CPG por programa académico

\* Programas académicos ofertados: Al menos 3 programas de pregrado