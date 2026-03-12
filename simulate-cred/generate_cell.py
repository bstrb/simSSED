# define your hard-coded defaults here:
AXIS_MAP = {
'monoclinic':    'b',
'tetragonal':    'c',
'hexagonal':     'c',
'trigonal':      'c',
'rhombohedral':  'c',
# orthorhombic, cubic, triclinic → no unique_axis entry
}
def write_cell_file(params, cell_path):
    """
    Write the parameters into a CrystFEL .cell file,
    auto-selecting unique_axis based on lattice_type.
    """

    # lookup (case-insensitive) and fall back to omitting the line
    lattice = params['lattice_type'].lower()
    unique = AXIS_MAP.get(lattice)

    with open(cell_path, 'w') as f:
        f.write("CrystFEL unit cell file version 1.0\n\n")
        f.write(f"lattice_type = {params['lattice_type']}\n")
        f.write(f"centering     = {params['centering']}\n")
        if unique:
            f.write(f"unique_axis   = {unique}\n\n")
        else:
            f.write("\n")

        f.write(f"a = {params['a']:.4f} A\n")
        f.write(f"b = {params['b']:.4f} A\n")
        f.write(f"c = {params['c']:.4f} A\n")
        f.write(f"al = {params['alpha']:.2f} deg\n")
        f.write(f"be = {params['beta']:.2f} deg\n")
        f.write(f"ga = {params['gamma']:.2f} deg\n")
    
    
    print(f"→ Wrote {cell_path}")
