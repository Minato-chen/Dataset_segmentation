import os
import random
import shutil

def collect_image_paths(data_dir):
    image_paths = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
    return image_paths


def create_output_dirs(output_dir, num_dirs):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_dirs):
        os.makedirs(os.path.join(output_dir, str(i)), exist_ok=True)


def distribute_images(image_paths, output_dir, num_dirs=7):
    random.shuffle(image_paths)
    chunk_size = len(image_paths) // num_dirs
    chunks = [image_paths[i * chunk_size:(i + 1) * chunk_size] for i in range(num_dirs)]

    # Add remaining images to the last chunk
    remainder = len(image_paths) % num_dirs
    if remainder:
        chunks[-1].extend(image_paths[-remainder:])

    for i, chunk in enumerate(chunks):
        dir_path = os.path.join(output_dir, str(i))
        for image_path in chunk:
            shutil.copy(image_path, dir_path)

    return chunks


def main():
    # Use os.getcwd() to get the current working directory
    project_dir = os.getcwd()
    data_dir = os.path.join(project_dir, 'data')
    output_dir = os.path.join(project_dir, 'seg_result')

    # Step 1: Collect all image paths
    image_paths = collect_image_paths(data_dir)
    print(f"Collected {len(image_paths)} images from {data_dir}")

    # Step 2: Create output directories
    create_output_dirs(output_dir, 7)
    print(f"Created output directories in {output_dir}")

    # Step 3: Distribute images into 7 directories
    chunks = distribute_images(image_paths, output_dir, num_dirs=7)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i} has {len(chunk)} images.")


if __name__ == "__main__":
    main()
