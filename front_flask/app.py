"""
app.py — El ensamblador del FRONT (Flask + Jinja2).

El front no tiene negocio ni base de datos: rutas que muestran HTML y un
cliente HTTP que habla con la API. Su único estado es la SESIÓN.
"""

import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import cliente_api

app = Flask(__name__)
# La clave que FIRMA la cookie de sesión viaja por variable de entorno:
app.secret_key = os.environ.get("CLAVE_SESION", "clave-solo-para-desarrollo")


def login_requerido(vista):
    """Sin sesión, toda ruta devuelve al login (RF1)."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura


# ── Autenticación ────────────────────────────────────────────────────


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ok, mensaje = cliente_api.verificar_credenciales(
            request.form.get("usuario", ""), request.form.get("contrasena", "")
        )
        if ok:
            session["usuario"] = request.form["usuario"]
            return redirect(url_for("listar"))
        flash(mensaje, "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def inicio():
    destino = "listar" if "usuario" in session else "login"
    return redirect(url_for(destino))


# ── Productos (la rebanada de la v6) ────────────────────────────────


@app.route("/productos")
@login_requerido
def listar():
    ok, productos, errores = cliente_api.listar_productos()
    for e in errores:
        flash(e, "error")
    return render_template("productos/lista.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_requerido
def crear():
    if request.method == "POST":
        datos = {
            "codigo": request.form.get("codigo", "").strip(),
            "nombre": request.form.get("nombre", "").strip(),
            "stock": request.form.get("stock", ""),
            "valorunitario": request.form.get("valorunitario", ""),
        }
        ok, errores = cliente_api.crear_producto(datos)
        if ok:
            flash(f"Producto {datos['codigo']} creado.", "exito")
            return redirect(url_for("listar"))
        for e in errores:
            flash(e, "error")
        return render_template("productos/formulario.html", producto=datos, editando=False)
    return render_template("productos/formulario.html", producto={}, editando=False)


@app.route("/productos/<codigo>/editar", methods=["GET", "POST"])
@login_requerido
def editar(codigo):
    if request.method == "POST":
        # PATCH: viaja SOLO lo diligenciado (dejar vacío = no tocar)
        datos = {
            campo: valor
            for campo, valor in {
                "nombre": request.form.get("nombre", "").strip(),
                "stock": request.form.get("stock", "").strip(),
                "valorunitario": request.form.get("valorunitario", "").strip(),
            }.items()
            if valor != ""
        }
        ok, errores = cliente_api.actualizar_producto(codigo, datos)
        if ok:
            flash(f"Producto {codigo} actualizado.", "exito")
            return redirect(url_for("listar"))
        for e in errores:
            flash(e, "error")
    ok, producto, errores = cliente_api.obtener_producto(codigo)
    if not ok:
        for e in errores:
            flash(e, "error")
        return redirect(url_for("listar"))
    return render_template("productos/formulario.html", producto=producto, editando=True)


@app.route("/productos/<codigo>/eliminar", methods=["POST"])
@login_requerido
def eliminar(codigo):
    ok, errores = cliente_api.eliminar_producto(codigo)
    if ok:
        flash(f"Producto {codigo} eliminado.", "exito")
    for e in errores:
        flash(e, "error")
    return redirect(url_for("listar"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PUERTO", "8049")))
