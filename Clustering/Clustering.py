import base64
from io import BytesIO
import tmap as tm
import pandas as pd
import numpy as np
from faerun import Faerun
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ======================
# 1. Cargar Fashion-MNIST
# ======================
df = pd.read_csv('Analisis_algoritmos/Clustering/fashion-mnist_test.csv')
IMAGES_TEST = df.iloc[:, 1:].values.astype(np.uint8)
LABELS_TEST = df['label'].values.astype(np.uint8)

# ======================
# 2. Seleccionar el cluster principal (por ejemplo: 5 = Sandal)
# ======================
cluster_label = 5
mask = LABELS_TEST == cluster_label
subset_images = IMAGES_TEST[mask]
subset_labels = LABELS_TEST[mask]
labels = [
    ("T-shirt/top"), 
    ("Trouser"), 
    ("Pullover"), 
    ("Dress"), 
    ("Coat"),
    ("Sandal"), 
    ("Shirt"), 
    ("Sneaker"), 
    ("Bag"), 
    ("Ankle boot")
]

print(f"Se seleccionaron {len(subset_images)} imágenes del cluster {cluster_label}")

# ======================
# 3. Aplicar TMAP al subset
# ======================
CFG = tm.LayoutConfiguration()
CFG.node_size = 1/50

dims = 512
enc = tm.Minhash(28*28, 42, dims)
lf = tm.LSHForest(dims * 2, 128)

tmp = [tm.VectorFloat(img / 255) for img in subset_images]

lf.batch_add(enc.batch_from_weight_array(tmp))
lf.index()

x, y, s, t, _ = tm.layout_from_lsh_forest(lf, CFG)

# ======================
# 4. Agrupar con KMeans
# ======================
coords = np.column_stack((x, y))

# Puedes cambiar n_clusters para controlar cuántos subclusters quieres
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
subcluster_labels = kmeans.fit_predict(coords)

print(f"Se detectaron {num_clusters} subclusters con KMeans")

# ======================
# 5. Crear etiquetas de imagen (para Faerun)
# ======================
image_labels = []
for image in subset_images:
    img = Image.fromarray(np.uint8(np.split(np.array(image), 28)))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    image_labels.append("data:image/jpeg;base64," + img_str)

# ======================
# 6. Crear leyenda con nombres para los subclusters
# ======================
legend_labels = [(i, f"Subcluster {i}") for i in range(num_clusters)]

# ======================
# 7. Visualización con Faerun
# ======================
faerun = Faerun(clear_color="#111111", view="front", coords=False)
faerun.add_scatter(
    f"FMNIST_sub_{labels[cluster_label]}",
    {
        "x": x,
        "y": y,
        "c": subcluster_labels,
        "labels": image_labels
    },
    colormap="tab10",
    shader="smoothCircle",
    point_scale=2.5,
    max_point_size=10,
    has_legend=True,
    categorical=True,
    legend_labels=legend_labels
)
faerun.add_tree(f"FMNIST_sub_{labels[cluster_label]}_tree", {"from": s, "to": t},
                point_helper=f"FMNIST_sub_{labels[cluster_label]}", color="#666666")

faerun.plot(f"Analisis_algoritmos/Clustering/fmnist_sub_{labels[cluster_label]}", 
            template="url_image")

# ======================
# 8. Mostrar ejemplos representativos por subcluster
# ======================
fig, axes = plt.subplots(num_clusters, 5, figsize=(8, 2*num_clusters))

for row in range(num_clusters):
    sub_mask = subcluster_labels == row
    imgs_sub = subset_images[sub_mask]
    if len(imgs_sub) == 0:
        continue
    n_show = min(5, len(imgs_sub))
    chosen = np.random.choice(len(imgs_sub), n_show, replace=False)
    for j in range(n_show):
        ax = axes[row, j] if num_clusters > 1 else axes[j]
        ax.imshow(imgs_sub[chosen[j]].reshape(28, 28), cmap='gray')
        ax.axis('off')
    if num_clusters > 1:
        axes[row, 0].set_ylabel(f"Subcluster {row}", rotation=0, labelpad=40, size=10)

plt.suptitle(f"Ejemplos representativos de subclusters (Cluster {labels[cluster_label]})")
plt.tight_layout()
plt.show()
