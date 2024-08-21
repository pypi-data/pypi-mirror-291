#!/usr/bin/env python3

import pymupdf
import concurrent.futures
import os
import argparse

# FILENAME = "braidonhypnotism00brai.pdf"

def process_page(page_num, doc):

    page = doc.load_page(page_num)
    width, height = page.rect.width, page.rect.height
    # Define the transformation matrix for flipping around the Y-axis
    flip_matrix = pymupdf.Matrix(-4, 0, 0, 4, 0, 0)
    pixmap = page.get_pixmap(matrix=flip_matrix)
    # pixmap.save("debug_images/" + str(page_num) + ".png")
    # imgpdf = pixmap.tobytes()
    return (page_num, pixmap, width, height)

def flip_pdf_y_axis(input_path, output_path = None, batch_size=10):

    if (output_path is None):
        output_path = input_path.replace(".pdf", "_flipped.pdf")
        
    # Open the input PDF document
    doc = pymupdf.open(input_path)
    
    # Get the dimensions of the first page to compute the transformation matrix
    first_page = doc.load_page(0)

    # Prepare to create the flipped document
    flipped_doc = pymupdf.open()

    # Get the total number of pages
    num_pages = len(doc)
    # num_pages = 3

    # Create a thread pool executor
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     # Process pages in batches
    #     for i in range(0, num_pages, batch_size):
    #         print(i)
    #         batch_pages = range(i, min(i + batch_size, num_pages))
    #         for page_num in batch_pages:
    #             # Submit each page processing to the executor
    #             futures.append(executor.submit(process_page, page_num, doc, flip_matrix))
            
    #         # Wait for all futures in the current batch to complete
    #         for future in concurrent.futures.as_completed(futures):
    #             imgpdf = future.result()
    #             page = flipped_doc.new_page()
    #             page.insert_image(page.rect, stream=imgpdf)
    #         # Clear futures list for the next batch
    #         futures.clear()

    page = doc.load_page(0)
    width = page.rect.width
    height = page.rect.height

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        # Process pages in batches
        for i in range(0, num_pages, batch_size):
            print(i)
            batch_pages = range(i, min(i + batch_size, num_pages))
            
            # Submit each page processing to the executor
            for page_num in batch_pages:
                future = executor.submit(process_page, page_num, doc)
                futures.append(future)
            
            # Wait for all futures in the current batch to complete
            j = 0
            for future in futures:
                (pagenum, imgpdf, width, height) = future.result()
                page = flipped_doc.new_page(height=height, width=width)
                page.insert_image(page.rect, pixmap=imgpdf)
            
            # Clear futures list for the next batch
            futures.clear()

    # Save the modified document
    flipped_doc.save(output_path, deflate=False, expand=1)
    flipped_doc.close()
    doc.close()

# Example usage
# flip_pdf_y_axis("PDFS/"+FILENAME, "FLIPPED_PDFS/"+FILENAME)


def main():
    parser = argparse.ArgumentParser(description="Process an input file and optionally write to an output file.")
    parser.add_argument('input_file', help="The input file to process")
    parser.add_argument('-o', '--output', help="Optional output file name")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: The file {args.input_file} does not exist.")
        return

    flip_pdf_y_axis(args.input_file, args.output)

if __name__ == '__main__':
    main()