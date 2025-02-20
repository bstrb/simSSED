
# Create the content of the bash file
 = f"""indexamajig -i {lst_file_path} -g {geom_file_path} -p {cell_file_path} -j {num_threads} -o int_output.stream --indexing=file --fromfile-input-file={input_sol_file} --no-revalidate --no-retry --integration=rings --no-refine --no-half-pixel-shift --no-check-peaks --no-non-hits-in-stream --no-check-cell --peaks=cxi --min-peaks=15
"""

indexamajig -g /Users/xiaodong/Desktop/simulations/UOX/UOXsim.geom -i /Users/xiaodong/Desktop/simulations/UOX/simulation-30/list.lst -o /Users/xiaodong/Desktop/simulations/UOX/simulation-30/UOXsimUB_-512.5_-512.5.stream -p /Users/xiaodong/Desktop/simulations/UOX/UOX.cell -j 8 --no-revalidate --no-half-pixel-shift --peaks=peakfinder9 --min-snr=1 --min-snr-biggest-pix=1 --min-sig=3 --local-bg-radius=3 --indexing=file --fromfile-input-file=/Users/xiaodong/Desktop/simulations/UOX/simulation-30/UB_matrices.sol --integration=rings --int-radius=4,5,10 --no-non-hits-in-stream