#!/usr/bin/env python3

import csv
import os
import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Script para convertir componentes desde un CSV usando easyeda2kicad."
    )
    # Argumento obligatorio: archivo CSV
    parser.add_argument("csv_file", help="Ruta al archivo CSV")
    # Argumento opcional: directorio de salida (por defecto, easyeda-libs)
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="./easyeda-libs/libs",
        help="Directorio de salida (opcional). Por defecto: easyeda-libs/libs"
    )
    # Opción --update para añadir --overwrite
    parser.add_argument(
        "--update",
        action="store_true",
        help="Si se especifica, añade '--overwrite' a la ejecución de easyeda2kicad."
    )
    
    args = parser.parse_args()
    
    # Crear el directorio de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        with open(args.csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Leer la primera fila como cabecera
            try:
                header = next(reader)
            except StopIteration:
                print(f"El archivo '{args.csv_file}' está vacío o no contiene datos.")
                sys.exit(1)
            
            # Localizar el índice de la columna "LCSC" (ignorando mayúsculas/minúsculas)
            lcsc_col_index = None
            for i, col_name in enumerate(header):
                if col_name.strip().upper() == "LCSC":
                    lcsc_col_index = i
                    break
            
            if lcsc_col_index is None:
                print("No se encontró la columna 'LCSC' en la cabecera del CSV.")
                sys.exit(1)

            # Iterar sobre las filas restantes y usar el valor de la columna LCSC
            for row in reader:
                # Si la fila está vacía o no llega al índice de LCSC, omitir
                if not row or len(row) <= lcsc_col_index:
                    continue
                
                lcsc_id = row[lcsc_col_index].strip()
                
                # Si la columna está vacía, omitir
                if not lcsc_id:
                    continue
                
                # Construir el comando base
                command = [
                    "easyeda2kicad",
                    "--full",
                    f"--lcsc_id={lcsc_id}",
                    f"--output={args.output_dir}"
                ]
                
                # Si se ha especificado --update, añadimos --overwrite
                if args.update:
                    command.append("--overwrite")
                
                print(f"Ejecutando: {' '.join(command)}")
                subprocess.run(command)
                
    except FileNotFoundError:
        print(f"No se encontró el archivo CSV: {args.csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
