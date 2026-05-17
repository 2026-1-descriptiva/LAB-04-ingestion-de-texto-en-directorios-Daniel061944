# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    """
    Descomprime files/input.zip y genera los datasets CSV
    files/output/train_dataset.csv y files/output/test_dataset.csv
    """

    import zipfile
    from pathlib import Path

    import pandas as pd

    base_dir = Path("files")
    zip_path = base_dir / "input.zip"
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    # Crear carpeta de salida
    output_dir.mkdir(parents=True, exist_ok=True)

    # Descomprimir solo si no existe la carpeta input
    if not input_dir.exists():
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            names = zip_ref.namelist()

            # Si el zip ya contiene una carpeta input/, se extrae en files/
            if any(name.startswith("input/") for name in names):
                zip_ref.extractall(base_dir)
            else:
                # Si el zip contiene directamente train/ y test/,
                # se extrae dentro de files/input/
                input_dir.mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(input_dir)

    def make_dataset(split):
        rows = []

        for target in ["negative", "neutral", "positive"]:
            folder = input_dir / split / target

            for file_path in sorted(folder.glob("*.txt")):
                try:
                    phrase = file_path.read_text(encoding="utf-8").strip()
                except UnicodeDecodeError:
                    phrase = file_path.read_text(encoding="latin-1").strip()

                rows.append(
                    {
                        "phrase": phrase,
                        "target": target,
                    }
                )

        return pd.DataFrame(rows)

    train_dataset = make_dataset("train")
    test_dataset = make_dataset("test")

    train_dataset.to_csv(output_dir / "train_dataset.csv", index=False)
    test_dataset.to_csv(output_dir / "test_dataset.csv", index=False)