
 ***** CORRECT ***** (VERSION Jan 19, 2025  BUILT=20251103)  19-Feb-2026

 INPUT PARAMETER VALUES
 ----------------------
 SPACE_GROUP_NUMBER=  221 as used in the INTEGRATE step
 UNIT_CELL_CONSTANTS=    11.909    11.909    11.909  90.000  90.000  90.000 as used by INTEGRATE
 FRIEDEL'S_LAW=FALSE
 PROFILE_FITTING= TRUE 
 OVERLOAD=    660000     MINPK=  75.00000    WFAC1=  10.0
 INCLUDE_RESOLUTION_RANGE=    20.000     0.600
 NAME_TEMPLATE_OF_DATA_FRAMES=/mnt/i/FIB_milling_staircase/TPX_Cheetah/LTA_121522/Stair/LTA_re/LTA_t1/converted/?????.img SMV
 DATA_RANGE=       1     757
 ROTATION_AXIS=  0.146806  0.989165 -0.000940
 OSCILLATION_RANGE=  0.120000
 STARTING_ANGLE=   -45.000     STARTING_FRAME=       1
 X-RAY_WAVELENGTH=  0.019690
 INCIDENT_BEAM_DIRECTION=  0.000020  0.000019  1.000000
 FRACTION_OF_POLARIZATION=   0.500
 POLARIZATION_PLANE_NORMAL=  0.000000  0.000000  0.000000
 AIR=   0.00010
 DETECTOR=UNKNOWN
 SILICON=  0.402235 SENSOR_THICKNESS=  0.000000
 NUMBER OF DETECTOR SEGMENTS   1
 NX=   512  NY=   512    QX=  0.055000  QY=  0.055000
 ORGX=    243.90  ORGY=    249.33
 DETECTOR_DISTANCE=   443.464
 DIRECTION_OF_DETECTOR_X-AXIS=   1.00000   0.00000   0.00000
 DIRECTION_OF_DETECTOR_Y-AXIS=   0.00000   1.00000   0.00000
 BEAM_DIVERGENCE_E.S.D.=   0.013
 REFLECTING_RANGE_E.S.D.=   0.054
 MINIMUM_ZETA=     0.050
 MAXIMUM_ERROR_OF_SPOT_POSITION=   3.0
 MAXIMUM_ERROR_OF_SPINDLE_POSITION=   2.0
 MINIMUM_I/SIGMA=   3.0
 REFLECTIONS/CORRECTION_FACTOR=      50
 SNRC=  0.10 I/sigma for use in scaling factor determination
 STRICT_ABSORPTION_CORRECTION=FALSE 
 CORRECTIONS= DECAY MODULATION ABSORPTION                      
 TEST_RESOLUTION_RANGE=    10.000     5.000     MIN_RFL_Rmeas=    50     MAX_FAC_Rmeas=    2.00
 REFERENCE_DATA_SET=                                                  
 FIT_B-FACTOR_TO_REFERENCE_DATA_SET=FALSE 

   14373 REFLECTIONS ON FILE "INTEGRATE.HKL"
       0 CORRUPTED REFLECTION RECORDS (IGNORED)
       0 MATCHING REFLECTIONS SPECIFIED IN FILE "FILTER.HKL"
       0 REFLECTIONS INCOMPLETE OR OUTSIDE IMAGE RANGE       1 ...     757
       0 OVERLOADED REFLECTIONS (IGNORED)
       0 REFLECTIONS OUTSIDE ACCEPTED RESOLUTION RANGES
                OR TOO CLOSE TO ROTATION AXIS (IGNORED)
   14373 REFLECTIONS ACCEPTED



 ******************************************************************************
                      AUTOMATIC SPACE GROUP ASSIGNMENT
 ******************************************************************************

 XDS adopts the following approach.
 (1) it looks for possible symmetries of the crystal lattice
 (2) it computes a redundancy independent R-factor for all enantiomorphous
     point groups compatible with the observed lattice symmetry.
 (3) it selects the group which explains the intensity data at an acceptable,
     redundancy-independent R-factor (Rmeas, Rrim) using a minimum number of
     unique reflections.

 This approach does not test for the presence of screw axes. Consequently,
 orthorhombic cell axes will be specified in increasing length (following
 conventions), despite the possibility that different assignments for the
 cell axes could become necessary for space groups P222(1) and P2(1)2(1)2
 containing one or two screw axes, respectively.

 The user can always override the automatic decisions by specifying the
 correct space group number and unit cell constants in XDS.INP and repeating
 the CORRECT step of XDS. This provides a simple way to rename orthorhombic
 cell constants if screw axes are present.

 In addition, the user has the option to specify in XDS.INP
 (a) a reference data set or
 (b) a reindexing transformation or
 (c) the three basis vectors (if known from processing a previous data set
 taken at the same crystal orientation in a multi-wavelength experiment).
 These features of XDS are useful for resolving the issue of alternative
 settings of polar or rhombohedral cells (like P4, P6, R3).

 =====> Specifications provided by the user in XDS.INP:
 SPACE_GROUP_NUMBER=  221 (0: unknown symmetry and unit cell)
 UNIT_CELL_CONSTANTS=    11.91    11.91    11.91  90.000  90.000  90.000
 UNIT_CELL_A-AXIS=     7.403    -4.953     7.905 (0 0 0 : unknown)
 UNIT_CELL_B-AXIS=     7.412     9.251    -1.146 (0 0 0 : unknown)
 UNIT_CELL_C-AXIS=    -5.664     5.633     8.833 (0 0 0 : unknown)
 REIDX=  0  0  0  0  0  0  0  0  0  0  0  0 (all 0 : not specified)
 TEST_RESOLUTION_RANGE=   10.00    5.00 (Angstrom) for space group determination
 NUMBER OF ACCEPTED REFLECTIONS FOR CALCULATING Rmeas               22
 NUMBER OF ACCEPTED UNIQUE REFLECTIONS FROM REFERENCE DATA SET       0


 *********** DETERMINATION OF LATTICE CHARACTER AND BRAVAIS LATTICE ***********

 The CHARACTER OF A LATTICE is defined by the metrical parameters of its
 reduced cell as described in the INTERNATIONAL TABLES FOR CRYSTALLOGRAPHY
 Volume A, p. 746 (KLUWER ACADEMIC PUBLISHERS, DORDRECHT/BOSTON/LONDON, 1989).
 Note that more than one lattice character may have the same BRAVAIS LATTICE.

 A lattice character is marked "*" to indicate a lattice consistent with the
 observed locations of the diffraction spots. These marked lattices must have
 low values for the QUALITY OF FIT and their implicated UNIT CELL CONSTANTS
 should not violate the ideal values by more than
 MAX_CELL_AXIS_ERROR=  0.03
 MAX_CELL_ANGLE_ERROR=           2.0 (Degrees)

 The REINDEXING TRANSFORMATION REIDX() consists of 12 integers that relate
 the original indices H,K,L from file INTEGRATE.HKL to the indices H',K',L'
 with respect to the new cell.
    H'=(REIDX(1)*H+REIDX( 2)*K+REIDX( 3)*L)/IDXV+REIDX( 4)
    K'=(REIDX(5)*H+REIDX( 6)*K+REIDX( 7)*L)/IDXV+REIDX( 8)
    L'=(REIDX(9)*H+REIDX(10)*K+REIDX(11)*L)/IDXV+REIDX(12)
 The value of the integer IDXV depends on the lattice type used for
 specifying reflections on file INTEGRATE.HKL; IDXV is
 1 for a primitive,
 2 for a face or body centred,
 3 for a rhombohedral,
 4 for a lattice centred on all faces.
 IDXV is set by XDS and cannot be input by the user.

  LATTICE-  BRAVAIS-   QUALITY  UNIT CELL CONSTANTS (ANGSTROEM & DEGREES)    REINDEXING TRANSFORMATION
 CHARACTER  LATTICE     OF FIT      a      b      c   alpha  beta gamma

 *  31        aP          0.0      11.9   11.9   11.9  90.0  90.0  90.0    0  0  1  0  1  0  0  0  0  1  0  0
 *  44        aP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *  35        mP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *  33        mP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *  10        mC          0.0      16.8   16.8   11.9  90.0  90.0  90.0    1  0  1  0 -1  0  1  0  0 -1  0  0
 *  13        oC          0.0      16.8   16.8   11.9  90.0  90.0  90.0   -1  0  1  0  1  0  1  0  0  1  0  0
 *  14        mC          0.0      16.8   16.8   11.9  90.0  90.0  90.0   -1  0  1  0  1  0  1  0  0  1  0  0
 *  34        mP          0.0      11.9   11.9   11.9  90.0  90.0  90.0    1  0  0  0  0 -1  0  0  0  0 -1  0
 *  11        tP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *  32        oP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *  20        mC          0.0      16.8   16.8   11.9  90.0  90.0  90.0    1  1  0  0  1 -1  0  0  0  0 -1  0
 *  23        oC          0.0      16.8   16.8   11.9  90.0  90.0  90.0    1 -1  0  0 -1 -1  0  0  0  0 -1  0
 *  25        mC          0.0      16.8   16.8   11.9  90.0  90.0  90.0    0  1  1  0  0  1 -1  0 -1  0  0  0
 *   2        hR          0.0      16.8   16.8   20.6  90.0  90.0 120.0   -1  0  1  0  0  1 -1  0 -1 -1 -1  0
 *   3        cP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
 *   4        hR          0.0      16.8   16.8   20.6  90.0  90.0 120.0   -1  0 -1  0  1  1  0  0  1 -1 -1  0
 *  21        tP          0.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
     5        cI        166.7      16.8   16.8   16.8  60.0  60.0  60.0    0 -1 -1  0  1  0 -1  0  1 -1  0  0
    28        mC        250.0      11.9   26.6   11.9  90.0  90.0  63.4    1  0  0  0  1 -2  0  0  0  0 -1  0
    30        mC        250.0      11.9   26.6   11.9  90.0  90.0  63.4    1  0  0  0  1 -2  0  0  0  0 -1  0
    40        oC        250.0      11.9   26.6   11.9  90.0  90.0 116.6   -1  0  0  0  1 -2  0  0  0  0  1  0
    36        oC        250.0      11.9   26.6   11.9  90.0  90.0 116.6   -1  0  0  0  1 -2  0  0  0  0  1  0
    41        mC        250.0      26.6   11.9   11.9  90.0  90.0  63.4   -1  2  0  0 -1  0  0  0  0  0  1  0
    37        mC        250.0      26.6   11.9   11.9  90.0  90.0  63.4   -1  2  0  0 -1  0  0  0  0  0  1  0
    39        mC        250.0      26.6   11.9   11.9  90.0  90.0  63.4   -2  0  1  0  0  0  1  0  0  1  0  0
    29        mC        250.0      11.9   26.6   11.9  90.0  90.0  63.4   -1  0  0  0 -1  0  2  0  0  1  0  0
    12        hP        250.0      11.9   11.9   11.9  90.0  90.0  90.0   -1  0  0  0  0  0  1  0  0  1  0  0
    38        oC        250.0      11.9   26.6   11.9  90.0  90.0 116.6    1  0  0  0 -1  0  2  0  0 -1  0  0
    22        hP        250.0      11.9   11.9   11.9  90.0  90.0  90.0    1  0  0  0  0 -1  0  0  0  0 -1  0
     1        cF        250.0      20.6   20.6   20.6 109.5 109.5 109.5   -1  1  1  0  1 -1  1  0  1  1 -1  0
    15        tI        500.0      11.9   11.9   29.2  65.9  65.9  90.0   -1  0  0  0  0  0  1  0 -1  2  1  0
    27        mC        500.0      26.6   11.9   16.8  90.0 129.2  63.4    2  0 -1  0  0  0 -1  0 -1  1  0  0
    42        oI        500.0      11.9   11.9   29.2 114.1 114.1  90.0    1  0  0  0  0  0 -1  0 -1  2  1  0
    19        oI        500.0      11.9   16.8   20.6  90.0  54.7  90.0    0  0 -1  0 -1  1  0  0  1  1 -1  0
    26        oF        625.0      11.9   26.6   26.6  78.5 116.6 116.6    0  0  1  0  2  0 -1  0  0  2 -1  0
    18        tI        625.0      16.8   20.6   11.9  54.7  90.0  90.0   -1  1  0  0 -1 -1  1  0  0  0  1  0
     9        hR        750.0      11.9   16.8   39.5  90.0 107.5 135.0    0  0  1  0  1  0 -1  0 -1  3 -1  0
     6        tI        999.0      16.8   16.8   16.8  60.0  60.0  60.0    0 -1  1  0  1 -1  0  0  1  0  1  0
     7        tI        999.0      16.8   16.8   16.8  60.0  60.0  60.0   -1  1  0  0 -1  0  1  0  0  1  1  0
     8        oI        999.0      16.8   16.8   16.8  60.0  60.0  60.0   -1  0 -1  0 -1  1  0  0  0  1 -1  0
    16        oF        999.0      16.8   16.8   29.2  90.0 125.3  90.0   -1  0 -1  0  1  0 -1  0  1 -2  1  0
    17        mC        999.0      16.8   16.8   16.8  60.0 120.0  90.0    1  0 -1  0 -1  0 -1  0 -1  1  0  0
    24        hR        999.0      29.2   16.8   11.9  90.0  65.9 106.8    1 -1 -2  0  1  0  1  0  0 -1  0  0
    43        mI        999.0      16.8   29.2   11.9 114.1 135.0  54.7   -1  1  0  0 -1  1  2  0  1  0  0  0

 ****** LATTICE SYMMETRY IMPLICATED BY SPACE GROUP SYMMETRY ******

BRAVAIS-            POSSIBLE SPACE-GROUPS FOR PROTEIN CRYSTALS
  TYPE                     [SPACE GROUP NUMBER,SYMBOL]
  aP      [1,P1]
  mP      [3,P2] [4,P2(1)]
 mC,mI    [5,C2]
  oP      [16,P222] [17,P222(1)] [18,P2(1)2(1)2] [19,P2(1)2(1)2(1)]
  oC      [21,C222] [20,C222(1)]
  oF      [22,F222]
  oI      [23,I222] [24,I2(1)2(1)2(1)]
  tP      [75,P4] [76,P4(1)] [77,P4(2)] [78,P4(3)] [89,P422] [90,P42(1)2]
          [91,P4(1)22] [92,P4(1)2(1)2] [93,P4(2)22] [94,P4(2)2(1)2]
          [95,P4(3)22] [96,P4(3)2(1)2]
  tI      [79,I4] [80,I4(1)] [97,I422] [98,I4(1)22]
  hP      [143,P3] [144,P3(1)] [145,P3(2)] [149,P312] [150,P321] [151,P3(1)12]
          [152,P3(1)21] [153,P3(2)12] [154,P3(2)21] [168,P6] [169,P6(1)]
          [170,P6(5)] [171,P6(2)] [172,P6(4)] [173,P6(3)] [177,P622]
          [178,P6(1)22] [179,P6(5)22] [180,P6(2)22] [181,P6(4)22] [182,P6(3)22]
  hR      [146,R3] [155,R32]
  cP      [195,P23] [198,P2(1)3] [207,P432] [208,P4(2)32] [212,P4(3)32]
          [213,P4(1)32]
  cF      [196,F23] [209,F432] [210,F4(1)32]
  cI      [197,I23] [199,I2(1)3] [211,I432] [214,I4(1)32]


 Several solutions exist for the given space group that explain the data. The
 selected solution (marked "*") correlates best with the given reference data set.
 The independent settings of the cell can be obtained by application of the
 REINDEXING TRANSFORMATION to the original indices H,K,L from file INTEGRATE.HKL

 CORRELATION = correlation factor with the reference data set
 NPAIR       = number of unique reflection pairs correlated 
 Rmeas=Rrim  = redundancy independent R-factor (intensities)
               For definition see:
               Rmeas : Diederichs & Karplus,
                       Nature Struct. Biol. 4, 269-275 (1997);
               Rrim  : Weiss & Hilgenfeld,
                       J.Appl.Cryst. 30,203-205 (1997).
 COMPARED    = number of reflections used for calculating Rmeas
 ESD         = Agreement with given unit cell geometry

 CORRELATION  NPAIR  Rmeas  COMPARED  ESD       REINDEX TRANSFORMATION

  *   0.00        0   12.1      18    0.00  1  0  0  0  0  1  0  0  0  0  1  0

 ************ SELECTED SPACE GROUP AND UNIT CELL FOR THIS DATA SET ************

 SPACE_GROUP_NUMBER=  221
 UNIT_CELL_CONSTANTS=    11.91    11.91    11.91  90.000  90.000  90.000
 UNIT_CELL_A-AXIS=     7.408    -4.951     7.902
 UNIT_CELL_B-AXIS=     7.405     9.257    -1.142
 UNIT_CELL_C-AXIS=    -5.667     5.623     8.836
 REFLECTIONS H,K,L FROM "INTEGRATE.HKL" WILL BE REINDEXED BY
 H' = (  1*H +  0*K +  0*L)/ 1 +  0
 K' = (  0*H +  1*K +  0*L)/ 1 +  0
 L' = (  0*H +  0*K +  1*L)/ 1 +  0

 ***** 48 EQUIVALENT POSITIONS IN SPACE GROUP #221 *****

    If x',y',z' is an equivalent position to x,y,z, then
        x'=x*ML(1)+y*ML( 2)+z*ML( 3)+ML( 4)/12.0
        y'=x*ML(5)+y*ML( 6)+z*ML( 7)+ML( 8)/12.0
        z'=x*ML(9)+y*ML(10)+z*ML(11)+ML(12)/12.0

    #    1  2  3  4    5  6  7  8    9 10 11 12 
    1    1  0  0  0    0  1  0  0    0  0  1  0
    2    0  0  1  0    1  0  0  0    0  1  0  0
    3    0  1  0  0    0  0  1  0    1  0  0  0
    4    1  0  0  0    0 -1  0  0    0  0 -1  0
    5    0  0  1  0   -1  0  0  0    0 -1  0  0
    6    0  1  0  0    0  0 -1  0   -1  0  0  0
    7   -1  0  0  0    0  1  0  0    0  0 -1  0
    8    0  0 -1  0    1  0  0  0    0 -1  0  0
    9    0 -1  0  0    0  0  1  0   -1  0  0  0
   10   -1  0  0  0    0 -1  0  0    0  0  1  0
   11    0  0 -1  0   -1  0  0  0    0  1  0  0
   12    0 -1  0  0    0  0 -1  0    1  0  0  0
   13    1  0  0  0    0  0  1  0    0  1  0  0
   14    0  1  0  0    1  0  0  0    0  0  1  0
   15    0  0  1  0    0  1  0  0    1  0  0  0
   16    1  0  0  0    0  0 -1  0    0 -1  0  0
   17    0  1  0  0   -1  0  0  0    0  0 -1  0
   18    0  0  1  0    0 -1  0  0   -1  0  0  0
   19   -1  0  0  0    0  0  1  0    0 -1  0  0
   20    0 -1  0  0    1  0  0  0    0  0 -1  0
   21    0  0 -1  0    0  1  0  0   -1  0  0  0
   22   -1  0  0  0    0  0 -1  0    0  1  0  0
   23    0 -1  0  0   -1  0  0  0    0  0  1  0
   24    0  0 -1  0    0 -1  0  0    1  0  0  0
   25   -1  0  0  0    0 -1  0  0    0  0 -1  0
   26    0  0 -1  0   -1  0  0  0    0 -1  0  0
   27    0 -1  0  0    0  0 -1  0   -1  0  0  0
   28   -1  0  0  0    0  1  0  0    0  0  1  0
   29    0  0 -1  0    1  0  0  0    0  1  0  0
   30    0 -1  0  0    0  0  1  0    1  0  0  0
   31    1  0  0  0    0 -1  0  0    0  0  1  0
   32    0  0  1  0   -1  0  0  0    0  1  0  0
   33    0  1  0  0    0  0 -1  0    1  0  0  0
   34    1  0  0  0    0  1  0  0    0  0 -1  0
   35    0  0  1  0    1  0  0  0    0 -1  0  0
   36    0  1  0  0    0  0  1  0   -1  0  0  0
   37   -1  0  0  0    0  0 -1  0    0 -1  0  0
   38    0 -1  0  0   -1  0  0  0    0  0 -1  0
   39    0  0 -1  0    0 -1  0  0   -1  0  0  0
   40   -1  0  0  0    0  0  1  0    0  1  0  0
   41    0 -1  0  0    1  0  0  0    0  0  1  0
   42    0  0 -1  0    0  1  0  0    1  0  0  0
   43    1  0  0  0    0  0 -1  0    0  1  0  0
   44    0  1  0  0   -1  0  0  0    0  0  1  0
   45    0  0  1  0    0 -1  0  0    1  0  0  0
   46    1  0  0  0    0  0  1  0    0 -1  0  0
   47    0  1  0  0    1  0  0  0    0  0 -1  0
   48    0  0  1  0    0  1  0  0   -1  0  0  0

 ******************************************************************************
      MEAN DISCREPANCIES BETWEEN OBSERVED AND CALCULATED SPOT LOCATIONS
 ******************************************************************************

 The discrepancies in X- and Y-coordinates of the spots are depicted in the
 two images DX-CORRECTIONS.cbf and DY-CORRECTIONS.cbf for inspection with
 the XDS-Viewer.


 !!! ERROR !!! CANNOT READ X-CORRECTIONS.cbf
               UNABLE TO CARRY OUT DIAGNOSTICS OF GEOMETRICAL DISTORTIONS
               OF THE DETECTOR. XDS WILL CONTINUE.



 ******************************************************************************
  REFINEMENT OF DIFFRACTION PARAMETERS USING ALL IMAGES
 ******************************************************************************


 REFINED VALUES OF DIFFRACTION PARAMETERS DERIVED FROM     13246 INDEXED SPOTS
 REFINED PARAMETERS:   AXIS ORIENTATION POSITION
 STANDARD DEVIATION OF SPOT    POSITION (PIXELS)     1.24
 STANDARD DEVIATION OF SPINDLE POSITION (DEGREES)    0.14
 SPACE GROUP NUMBER    221
 UNIT CELL PARAMETERS     11.909    11.909    11.909  90.000  90.000  90.000
 E.S.D. OF CELL PARAMETERS -1.0E+00-1.0E+00-1.0E+00-1.0E+00-1.0E+00-1.0E+00
 REC. CELL PARAMETERS   0.083968  0.083968  0.083968  90.000  90.000  90.000
 COORDINATES OF UNIT CELL A-AXIS     7.405    -4.951     7.905
 COORDINATES OF UNIT CELL B-AXIS     7.410     9.252    -1.146
 COORDINATES OF UNIT CELL C-AXIS    -5.664     5.631     8.834
 CRYSTAL MOSAICITY (DEGREES)     0.054
 LAB COORDINATES OF ROTATION AXIS  0.153902  0.988085 -0.001411
 DIRECT BEAM COORDINATES (REC. ANGSTROEM)   0.000000  0.000000 50.787209
 DETECTOR COORDINATES (PIXELS) OF DIRECT BEAM     243.99    249.38
 DETECTOR ORIGIN (PIXELS) AT                      243.99    249.38
 CRYSTAL TO DETECTOR DISTANCE (mm)       444.57
 LAB COORDINATES OF DETECTOR X-AXIS  1.000000  0.000000  0.000000
 LAB COORDINATES OF DETECTOR Y-AXIS  0.000000  1.000000  0.000000


 THE DATA COLLECTION STATISTICS REPORTED BELOW ASSUMES:
 SPACE_GROUP_NUMBER=  221
 UNIT_CELL_CONSTANTS=    11.91    11.91    11.91  90.000  90.000  90.000


 ******************************************************************************
        MEAN INTENSITY AS FUNCTION OF SPINDLE POSITION WITHIN DATA IMAGE
 ******************************************************************************

 This statistics could serve as a diagnostic tool for detecting
 shutter problems (suggested by Kay Diederichs).
 Data are corrected for this effect if PATCH_SHUTTER_PROBLEM=TRUE in XDS.INP.
 ===> Selected : PATCH_SHUTTER_PROBLEM=FALSE

 INTERVAL = Angular interval in units of the oscillation range
            covered by a data image.
 NUMBER   = Number of reflections in each interval
 INTENSITY= Mean intensity of the reflections in each interval
 FACTOR   = Correction factor applied to intensities;
            INTENSITY(overall)/INTENSITY(interval)

   INTERVAL     NUMBER      INTENSITY      FACTOR
 -0.05  0.05      1406        117.470       0.993
  0.05  0.15      1479        122.539       0.952
  0.15  0.25      1423        111.005       1.051
  0.25  0.35      1468        126.623       0.922
  0.35  0.45      1421        119.886       0.973
  0.45  0.55      1424        119.245       0.979
  0.55  0.65      1421        103.315       1.130
  0.65  0.75      1411        107.784       1.083
  0.75  0.85      1459        118.563       0.984
  0.85  0.95      1461        119.880       0.974

 -0.05  0.95     14373        116.707       1.000


 ******************************************************************************
           CORRECTION FACTORS AS FUNCTION OF IMAGE NUMBER & RESOLUTION
 ******************************************************************************

 RECIPROCAL CORRECTION FACTORS FOR INPUT DATA SETS MERGED TO
 OUTPUT FILE: XDS_ASCII.HKL                                     

 THE CALCULATIONS ASSUME         FRIEDEL'S_LAW= TRUE
 TOTAL NUMBER OF CORRECTION FACTORS DEFINED      272
 DEGREES OF FREEDOM OF CHI^2 FIT             13473.0
 CHI^2-VALUE OF FIT OF CORRECTION FACTORS      0.860
 NUMBER OF CYCLES CARRIED OUT                      3

 CORRECTION FACTORS for visual inspection by XDS-Viewer DECAY.cbf           
 XMIN=     0.4 XMAX=   752.9 NXBIN=   17
 YMIN= 0.00705 YMAX= 2.76386 NYBIN=   16
 NUMBER OF REFLECTIONS USED FOR DETERMINING CORRECTION FACTORS      14342


 ******************************************************************************
  CORRECTION FACTORS AS FUNCTION OF X (fast) & Y(slow) IN THE DETECTOR PLANE
 ******************************************************************************

 RECIPROCAL CORRECTION FACTORS FOR INPUT DATA SETS MERGED TO
 OUTPUT FILE: XDS_ASCII.HKL                                     

 THE CALCULATIONS ASSUME         FRIEDEL'S_LAW= TRUE
 TOTAL NUMBER OF CORRECTION FACTORS DEFINED      289
 DEGREES OF FREEDOM OF CHI^2 FIT             13468.3
 CHI^2-VALUE OF FIT OF CORRECTION FACTORS      0.858
 NUMBER OF CYCLES CARRIED OUT                      3

 CORRECTION FACTORS for visual inspection by XDS-Viewer MODPIX.cbf          
 XMIN=     4.3 XMAX=   506.9 NXBIN=   17
 YMIN=     5.4 YMAX=   506.4 NYBIN=   17
 NUMBER OF REFLECTIONS USED FOR DETERMINING CORRECTION FACTORS      14342


 ******************************************************************************
   CORRECTION FACTORS AS FUNCTION OF IMAGE NUMBER & DETECTOR SURFACE POSITION
 ******************************************************************************

 RECIPROCAL CORRECTION FACTORS FOR INPUT DATA SETS MERGED TO
 OUTPUT FILE: XDS_ASCII.HKL                                     

 THE CALCULATIONS ASSUME         FRIEDEL'S_LAW= TRUE
 TOTAL NUMBER OF CORRECTION FACTORS DEFINED      221
 DEGREES OF FREEDOM OF CHI^2 FIT             13473.0
 CHI^2-VALUE OF FIT OF CORRECTION FACTORS      0.857
 NUMBER OF CYCLES CARRIED OUT                      3

 CORRECTION FACTORS for visual inspection by XDS-Viewer ABSORP.cbf          
 XMIN=     0.4 XMAX=   752.9 NXBIN=   17
 DETECTOR_SURFACE_POSITION=     256     256
 DETECTOR_SURFACE_POSITION=     341     341
 DETECTOR_SURFACE_POSITION=     170     341
 DETECTOR_SURFACE_POSITION=     170     171
 DETECTOR_SURFACE_POSITION=     341     171
 DETECTOR_SURFACE_POSITION=     449     336
 DETECTOR_SURFACE_POSITION=     336     448
 DETECTOR_SURFACE_POSITION=     176     448
 DETECTOR_SURFACE_POSITION=      62     336
 DETECTOR_SURFACE_POSITION=      62     176
 DETECTOR_SURFACE_POSITION=     176      63
 DETECTOR_SURFACE_POSITION=     336      63
 DETECTOR_SURFACE_POSITION=     449     176
 NUMBER OF REFLECTIONS USED FOR DETERMINING CORRECTION FACTORS      14342


 ******************************************************************************
    CORRECTION PARAMETERS FOR THE STANDARD ERROR OF REFLECTION INTENSITIES
 ******************************************************************************

 The variance v0(I) of the intensity I obtained from counting statistics is
 replaced by v(I)=a*(v0(I)+b*I^2). The model parameters a, b are chosen to
 minimize the discrepancies between v(I) and the variance estimated from
 sample statistics of symmetry related reflections. This model implicates
 an asymptotic limit ISa=1/SQRT(a*b) for the highest I/Sigma(I) that the
 experimental setup can produce (Diederichs (2010) Acta Cryst D66, 733-740).

     a        b          ISa
 1.393E+02  1.042E-03    2.63


 ******************************************************************************
      STANDARD ERROR OF REFLECTION INTENSITIES AS FUNCTION OF RESOLUTION
      FOR DATA SET  XDS_ASCII.HKL                                     
 ******************************************************************************

  I/Sigma  = mean intensity/Sigma of a reflection in shell
  Chi^2    = goodness of fit between sample variances of
             symmetry-related intensities and their errors
             (Chi^2 = 1 for perfect agreement)
  R-FACTOR
  observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
  expected = expected R-FACTOR derived from Sigma(I)

   NUMBER  = number of reflections in resolution shell
             used for calculation of R-FACTOR
  ACCEPTED = number of accepted reflections
  REJECTED = number of rejected reflections (MISFITS),
             recognized by comparison with symmetry-related
             reflections.

 RESOLUTION RANGE  I/Sigma  Chi^2  R-FACTOR  R-FACTOR  NUMBER ACCEPTED REJECTED
                                   observed  expected

   11.909   4.669     2.62   0.48     12.44     27.31      29      29       0
    4.669   3.436     2.62   0.48     20.33     28.76      44      44       0
    3.436   2.845     2.62   0.34     17.57     29.27      55      55       0
    2.845   2.482     2.55   0.60     23.77     29.11      66      66       0
    2.482   2.229     2.49   0.78     28.64     28.54      75      75       0
    2.229   2.041     2.39   1.22     36.82     29.84     103     103       0
    2.041   1.894     2.50   0.79     25.62     29.50      79      79       0
    1.894   1.774     2.53   1.44     35.36     29.82     130     130       0
    1.774   1.675     2.44   1.59     28.39     29.27      84      84       0
    1.675   1.590     2.47   1.01     27.48     29.82     128     128       0
    1.590   1.518     2.52   0.88     19.32     29.65      97      97       0
    1.518   1.454     2.44   1.68     33.25     29.58     146     146       0
    1.454   1.398     2.52   0.83     21.82     29.77     117     117       0
    1.398   1.348     2.51   0.99     22.54     29.99     175     175       0
    1.348   1.302     2.49   0.73     23.84     29.50     110     110       0
    1.302   1.262     2.44   0.99     32.18     30.46     185     185       0
    1.262   1.224     2.49   1.17     37.75     30.48     145     145       0
    1.224   1.190     2.52   0.91     22.08     29.31     135     135       0
    1.190   1.159     2.45   0.90     28.29     30.44     182     182       0
    1.159   1.130     2.47   0.88     24.03     29.87     175     175       0
    1.130   1.103     2.17   1.44     33.58     30.58     150     150       0
    1.103   1.078     1.92   1.66     61.93     34.46     201     201       0
    1.078   1.054     2.14   1.52     52.05     33.43     162     162       0
    1.054   1.032     2.19   1.53     44.54     31.64     204     204       0
    1.032   1.011     2.18   1.36     35.67     31.07     188     188       0
    1.011   0.992     2.18   1.36     49.83     31.86     135     135       0
    0.992   0.973     2.05   1.26     42.21     32.21     251     251       0
    0.973   0.956     2.18   1.20     43.74     33.06     241     241       0
    0.956   0.939     2.08   1.20     34.09     31.48      90      90       0
    0.939   0.924     1.88   1.41     55.46     35.35     297     297       0
    0.924   0.909     1.90   1.16     42.74     33.52     186     186       0
    0.909   0.895     2.02   1.32     50.79     34.67     189     189       0
    0.895   0.881     2.14   1.00     37.12     33.32     267     267       0
    0.881   0.868     1.97   1.12     45.45     34.72     204     204       0
    0.868   0.856     2.03   0.90     40.43     33.12     132     132       0
    0.856   0.844     1.82   1.05     44.96     36.54     294     294       0
    0.844   0.832     1.87   1.03     46.50     37.20     212     212       0
    0.832   0.821     1.95   0.87     33.96     33.99     332     332       0
    0.821   0.811     1.96   0.89     36.42     34.86     150     150       0
    0.811   0.801     1.91   1.06     43.96     36.13     281     281       0
    0.801   0.791     1.96   0.98     43.25     36.13     202     202       0
    0.791   0.781     1.97   0.88     37.87     34.76     253     253       0
    0.781   0.772     1.77   0.84     38.05     36.94     296     296       0
    0.772   0.763     1.90   0.88     31.43     33.98     227     227       0
    0.763   0.755     1.52   0.72     46.61     44.62     226     226       0
    0.755   0.747     1.55   0.84     43.02     39.08     318     318       0
    0.747   0.739     1.51   0.91     41.57     39.47     177     177       0
    0.739   0.731     1.70   0.66     35.81     39.00     274     274       0
    0.731   0.724     1.79   0.81     33.61     35.52     362     362       0
    0.724   0.716     1.39   0.60     43.53     46.58     250     250       0
    0.716   0.709     1.66   0.69     32.76     36.11     241     241       0
    0.709   0.703     1.54   0.73     43.73     43.01     236     236       0
    0.703   0.696     1.52   0.77     40.11     39.24     243     243       0
    0.696   0.689     1.46   0.67     43.12     41.37     356     356       0
    0.689   0.683     1.46   0.64     44.50     47.60     237     237       0
    0.683   0.677     1.51   0.76     42.13     41.35     365     365       0
    0.677   0.671     1.48   0.65     40.57     44.84     262     262       0
    0.671   0.665     1.37   0.71     49.49     45.45     206     206       0
    0.665   0.660     1.34   0.64     42.38     45.40     311     311       0
    0.660   0.654     1.24   0.53     47.40     53.68     334     334       0
    0.654   0.649     1.03   0.47     54.34     65.99     168     168       0
    0.649   0.644     1.09   0.53     52.84     58.59     419     419       0
    0.644   0.638     1.42   0.47     37.68     46.36     183     183       0
    0.638   0.633     1.03   0.45     49.69     60.39     257     257       0
    0.633   0.629     1.15   0.49     45.29     54.41     237     237       0
    0.629   0.624     1.10   0.43     38.28     50.43     237     237       0
    0.624   0.619     1.03   0.45     50.87     62.68     256     256       0
    0.619   0.615     1.08   0.42     43.79     59.36     310     310       0
    0.615   0.610     1.06   0.31     26.27     47.09     206     206       0
    0.610   0.606     0.94   0.34     46.24     72.04     231     231       0
    0.606   0.602     0.97   0.36     47.13     61.97      64      67       0
   --------------------------------------------------------------------------
   11.909   0.602     1.76   0.86     30.56     31.96   14370   14373       0



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR VARIOUS SUBSETS OF INCLUDED DATA IMAGES
 ******************************************************************************

 Data set statistics is reported below several times, each with a different
 upper limit on the number of images included. This provides the user with
 the information for deciding which data images should be excluded from the
 final data set because of radiation damage or other defects. If the user
 decides for a subset of "good" images that differs from the specification
 as given by the input parameter (see DATA_RANGE= in XDS.INP) the CORRECT-
 step of XDS must be repeated with the new parameter values for DATA_RANGE=.


 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1      85
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79          65      23        51       45.1%      33.0%     27.0%       60    3.85     38.1%    86.1*     0    0.000       0
     1.27         112      37        68       54.4%      29.6%     26.2%      104    3.79     34.5%    94.5*     0    0.000       0
     1.04         160      50        84       59.5%      38.2%     27.6%      153    3.51     45.1%    80.7*     0    0.000       0
     0.90         173      52        93       55.9%      51.5%     30.3%      166    3.31     61.8%    26.5      0    0.000       0
     0.81         211      64        99       64.6%      35.9%     32.4%      196    3.13     41.1%    70.0*     0    0.000       0
     0.74         220      65       111       58.6%      31.3%     34.1%      209    2.77     36.3%    95.2*     0    0.000       0
     0.68         248      76       117       65.0%      35.6%     37.8%      232    2.51     41.7%    90.0*     0    0.000       0
     0.64         248      78       122       63.9%      43.7%     46.4%      230    1.88     51.4%    65.7*     0    0.000       0
     0.60         211      76       132       57.6%      41.0%     54.1%      186    1.50     48.6%    86.4*     0    0.000       0
    total        1648     521       877       59.4%      34.9%     29.1%     1536    2.70     40.8%    91.1*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      1648
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         1648
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    521



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     169
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         129      37        51       72.5%      28.1%     27.4%      122    4.26     31.4%    89.3*     0    0.000       0
     1.27         224      55        68       80.9%      22.7%     27.6%      220    4.43     25.3%    98.1*     0    0.000       0
     1.04         322      70        84       83.3%      29.7%     27.7%      320    4.19     33.5%    94.5*     0    0.000       0
     0.90         356      79        93       84.9%      43.8%     30.5%      349    3.82     49.2%    83.6*     0    0.000       0
     0.81         404      85        99       85.9%      33.3%     32.6%      399    3.78     37.0%    86.4*     0    0.000       0
     0.74         454      96       111       86.5%      30.8%     34.5%      446    3.36     34.6%    96.2*     0    0.000       0
     0.68         491     102       117       87.2%      33.8%     37.6%      486    3.04     37.8%    93.6*     0    0.000       0
     0.64         494     105       122       86.1%      41.3%     46.4%      484    2.40     45.8%    77.7*     0    0.000       0
     0.60         414     104       132       78.8%      39.1%     56.1%      396    1.79     44.6%    87.5*     0    0.000       0
    total        3288     733       877       83.6%      29.7%     29.8%     3222    3.26     33.2%    94.4*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      3288
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         3288
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    733



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     253
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         191      42        51       82.4%      26.9%     27.8%      185    4.90     29.6%    93.4*     0    0.000       0
     1.27         339      60        68       88.2%      23.1%     28.4%      336    5.25     25.1%    97.7*     0    0.000       0
     1.04         469      79        84       94.0%      28.3%     28.7%      468    4.85     31.0%    95.9*     0    0.000       0
     0.90         534      88        93       94.6%      42.5%     31.0%      531    4.32     46.6%    95.9*     0    0.000       0
     0.81         591      92        99       92.9%      34.3%     33.5%      591    4.33     37.3%    85.8*     0    0.000       0
     0.74         667     105       111       94.6%      33.7%     35.8%      666    3.84     36.8%    95.6*     0    0.000       0
     0.68         716     110       117       94.0%      32.4%     37.6%      713    3.53     35.4%    96.3*     0    0.000       0
     0.64         722     116       122       95.1%      40.5%     46.7%      715    2.80     44.0%    87.6*     0    0.000       0
     0.60         605     117       132       88.6%      39.2%     55.1%      593    2.09     43.4%    90.7*     0    0.000       0
    total        4834     809       877       92.2%      29.3%     30.5%     4798    3.76     32.1%    96.4*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      4834
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         4834
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    809



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     337
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         263      51        51      100.0%      24.3%     27.5%      261    5.25     26.6%    94.2*     0    0.000       0
     1.27         447      68        68      100.0%      25.2%     28.5%      443    5.67     27.2%    98.7*     0    0.000       0
     1.04         622      84        84      100.0%      29.7%     29.0%      621    5.50     32.0%    96.3*     0    0.000       0
     0.90         715      93        93      100.0%      44.5%     31.5%      714    4.86     48.0%    94.8*     0    0.000       0
     0.81         792      99        99      100.0%      37.0%     33.5%      792    4.79     39.7%    96.9*     0    0.000       0
     0.74         885     111       111      100.0%      36.8%     35.7%      885    4.35     39.6%    97.0*     0    0.000       0
     0.68         970     117       117      100.0%      38.0%     38.6%      970    3.98     41.1%    90.7*     0    0.000       0
     0.64         967     122       122      100.0%      42.3%     46.8%      966    3.22     45.4%    85.0*     0    0.000       0
     0.60         812     122       132       92.4%      40.9%     55.4%      808    2.40     44.5%    91.4*     0    0.000       0
    total        6473     867       877       98.9%      29.9%     30.6%     6460    4.24     32.3%    97.2*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      6473
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         6473
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    867



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     421
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         324      51        51      100.0%      24.3%     28.0%      324    5.84     26.7%    83.6*     0    0.000       0
     1.27         567      68        68      100.0%      24.6%     28.9%      567    6.45     26.2%    98.2*     0    0.000       0
     1.04         779      84        84      100.0%      32.2%     29.6%      779    6.12     34.2%    97.7*     0    0.000       0
     0.90         892      93        93      100.0%      43.8%     31.7%      892    5.39     46.6%    95.3*     0    0.000       0
     0.81         988      99        99      100.0%      40.7%     34.0%      988    5.34     43.2%    93.2*     0    0.000       0
     0.74        1107     111       111      100.0%      37.8%     36.1%     1107    4.91     40.0%    98.3*     0    0.000       0
     0.68        1213     117       117      100.0%      40.6%     39.3%     1213    4.42     43.0%    96.0*     0    0.000       0
     0.64        1208     122       122      100.0%      44.4%     46.9%     1208    3.62     47.0%    84.0*     0    0.000       0
     0.60        1002     123       132       93.2%      39.7%     54.7%      999    2.71     42.6%    99.0*     0    0.000       0
    total        8080     868       877       99.0%      30.5%     31.0%     8077    4.74     32.7%    93.0*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      8080
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         8080
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    868



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     505
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         375      51        51      100.0%      24.1%     28.3%      375    6.23     26.1%    85.5*     0    0.000       0
     1.27         671      68        68      100.0%      24.5%     29.1%      671    6.96     25.8%    99.0*     0    0.000       0
     1.04         928      84        84      100.0%      31.0%     29.9%      928    6.70     32.6%    96.5*     0    0.000       0
     0.90        1066      93        93      100.0%      43.5%     32.1%     1066    5.83     45.8%    96.2*     0    0.000       0
     0.81        1183      99        99      100.0%      40.1%     34.2%     1183    5.86     42.1%    94.4*     0    0.000       0
     0.74        1327     111       111      100.0%      37.0%     36.2%     1327    5.40     38.8%    98.0*     0    0.000       0
     0.68        1449     117       117      100.0%      39.4%     38.9%     1449    4.88     41.3%    98.2*     0    0.000       0
     0.64        1443     122       122      100.0%      44.3%     47.2%     1443    3.95     46.5%    90.1*     0    0.000       0
     0.60        1208     125       132       94.7%      40.0%     54.6%     1205    2.96     42.6%    94.8*     0    0.000       0
    total        9650     870       877       99.2%      30.2%     31.3%     9647    5.17     32.0%    94.2*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES      9650
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                         9650
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    870



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     589
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         432      51        51      100.0%      23.8%     28.6%      432    6.67     25.6%    86.3*     0    0.000       0
     1.27         779      68        68      100.0%      24.4%     29.4%      779    7.49     25.5%    98.6*     0    0.000       0
     1.04        1087      84        84      100.0%      31.1%     30.1%     1087    7.22     32.6%    97.3*     0    0.000       0
     0.90        1237      93        93      100.0%      43.1%     32.3%     1237    6.29     45.0%    97.0*     0    0.000       0
     0.81        1382      99        99      100.0%      40.1%     34.4%     1382    6.34     41.9%    94.6*     0    0.000       0
     0.74        1541     111       111      100.0%      37.6%     36.6%     1541    5.80     39.1%    98.3*     0    0.000       0
     0.68        1672     117       117      100.0%      38.1%     39.1%     1672    5.26     39.7%    97.3*     0    0.000       0
     0.64        1671     122       122      100.0%      43.6%     47.2%     1671    4.24     45.4%    89.4*     0    0.000       0
     0.60        1389     125       132       94.7%      40.4%     55.3%     1387    3.16     42.7%    94.6*     0    0.000       0
    total       11190     870       877       99.2%      30.1%     31.5%    11188    5.56     31.7%    94.3*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES     11190
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                        11190
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    870



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     673
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         495      51        51      100.0%      23.9%     28.8%      495    7.08     25.3%    90.7*     0    0.000       0
     1.27         887      68        68      100.0%      25.6%     29.6%      887    7.94     26.6%    98.6*     0    0.000       0
     1.04        1243      84        84      100.0%      30.9%     30.3%     1243    7.70     32.2%    96.9*     0    0.000       0
     0.90        1411      93        93      100.0%      42.7%     32.4%     1411    6.72     44.4%    97.0*     0    0.000       0
     0.81        1582      99        99      100.0%      40.2%     34.6%     1582    6.78     41.8%    86.4*     0    0.000       0
     0.74        1765     111       111      100.0%      38.0%     36.8%     1765    6.18     39.4%    99.0*     0    0.000       0
     0.68        1922     117       117      100.0%      38.4%     39.3%     1922    5.61     39.7%    97.0*     0    0.000       0
     0.64        1938     122       122      100.0%      43.5%     47.3%     1938    4.57     45.0%    97.1*     0    0.000       0
     0.60        1605     125       132       94.7%      41.0%     56.3%     1603    3.39     43.0%    95.2*     0    0.000       0
    total       12848     870       877       99.2%      30.4%     31.8%    12846    5.94     31.7%    95.9*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES     12848
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                        12848
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    870



 ******************************************************************************
  STATISTICS OF SAVED DATA SET "XDS_ASCII.HKL" (DATA_RANGE=       1     757)
 FILE TYPE:         XDS_ASCII      MERGE=FALSE          FRIEDEL'S_LAW=FALSE
 ******************************************************************************

   REFLECTIONS OF TYPE H,0,0  0,K,0  0,0,L OR EXPECTED TO BE ABSENT (*)
   --------------------------------------------------------------------

   H    K    L  RESOLUTION  INTENSITY     SIGMA    INTENSITY/SIGMA  #OBSERVED

    1    0    0    11.909   0.5688E+03  0.1547E+03         3.68           2 
    2    0    0     5.955   0.1083E+04  0.2137E+03         5.07           4 
    3    0    0     3.970   0.4696E+03  0.9150E+02         5.13           4 
    4    0    0     2.977   0.8019E+03  0.1652E+03         4.85           4 
    5    0    0     2.382   0.1802E+04  0.3630E+03         4.96           4 
    6    0    0     1.985   0.8039E+03  0.1553E+03         5.18           4 
    7    0    0     1.701   0.2180E+03  0.4771E+02         4.57           4 
    8    0    0     1.489   0.1834E+04  0.3527E+03         5.20           4 
    9    0    0     1.323   0.5754E+03  0.1122E+03         5.13           4 
   10    0    0     1.191   0.1966E+04  0.3760E+03         5.23           4 
   11    0    0     1.083   0.1455E+03  0.2968E+02         4.90           4 
   12    0    0     0.992   0.3353E+03  0.6622E+02         5.06           4 
   13    0    0     0.916   0.6503E+02  0.1419E+02         4.58           4 
   14    0    0     0.851   0.2051E+02  0.6330E+01         3.24           4 
   15    0    0     0.794   0.6729E+02  0.1663E+02         4.05           3 
   16    0    0     0.744   0.4970E+03  0.1114E+03         4.46           3 
   17    0    0     0.701   0.1126E+03  0.2697E+02         4.18           3 
   18    0    0     0.662   0.1776E+02  0.6398E+01         2.78           3 
   19    0    0     0.627   0.9559E+00  0.2695E+01         0.35           3 

          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.

       NOTE:      Friedel pairs are treated as different reflections.

 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     1.79         550      51        51      100.0%      23.6%     29.1%      550    7.49     25.0%    84.3*     0    0.000       0
     1.27         995      68        68      100.0%      25.8%     29.8%      995    8.42     26.8%    97.9*     0    0.000       0
     1.04        1389      84        84      100.0%      31.3%     30.4%     1389    8.14     32.4%    97.1*     0    0.000       0
     0.90        1584      93        93      100.0%      42.8%     32.6%     1584    7.16     44.3%    98.7*     0    0.000       0
     0.81        1769      99        99      100.0%      40.6%     34.7%     1769    7.15     41.9%    96.6*     0    0.000       0
     0.74        1979     111       111      100.0%      38.9%     37.0%     1979    6.50     40.2%    99.0*     0    0.000       0
     0.68        2150     117       117      100.0%      38.3%     39.5%     2150    5.90     39.5%    95.4*     0    0.000       0
     0.64        2156     122       122      100.0%      44.4%     47.6%     2156    4.80     45.7%    95.9*     0    0.000       0
     0.60        1801     127       132       96.2%      41.9%     56.8%     1798    3.52     43.8%    94.7*     0    0.000       0
    total       14373     872       877       99.4%      30.6%     32.0%    14370    6.26     31.8%    93.5*     0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES     14373
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                        14373
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    872



 ******************************************************************************
    WILSON STATISTICS OF DATA SET  "XDS_ASCII.HKL"
 ******************************************************************************

 Data is divided into resolution shells and a straight line 
 A - 2*B*SS is fitted to log<I>, where
   RES    = mean resolution (Angstrom) in shell
   SS     = mean of (sin(THETA)/LAMBDA)**2 in shell
   <I>    = mean reflection intensity in shell
   BO     = (A - log<I>)/(2*SS)
    #     = number of reflections in resolution shell

   WILSON LINE (using all data) : A=   6.070 B=   2.894 CORRELATION=  0.98
      #      RES      SS        <I>       log(<I>)       BO
      22     3.512   0.020  5.8790E+02       6.377      -7.6
      27     2.085   0.058  2.8729E+02       5.660       3.6
      29     1.638   0.093  2.9681E+02       5.693       2.0
      35     1.389   0.130  2.1952E+02       5.391       2.6
      35     1.229   0.166  2.2878E+02       5.433       1.9
      38     1.117   0.200  1.3822E+02       4.929       2.8
      42     1.028   0.236  8.1011E+01       4.395       3.5
      45     0.957   0.273  6.1073E+01       4.112       3.6
      49     0.897   0.311  4.8876E+01       3.889       3.5
      48     0.847   0.349  3.5034E+01       3.556       3.6
      48     0.807   0.384  4.5300E+01       3.813       2.9
      50     0.773   0.419  3.9828E+01       3.685       2.8
      54     0.742   0.455  2.9900E+01       3.398       2.9
      53     0.714   0.491  3.1900E+01       3.463       2.7
      62     0.689   0.527  2.2597E+01       3.118       2.8
      59     0.665   0.566  1.7952E+01       2.888       2.8
      58     0.645   0.601  1.1831E+01       2.471       3.0
      63     0.626   0.638  1.2056E+01       2.490       2.8
      55     0.610   0.672  1.1607E+01       2.452       2.7


 HIGHER ORDER MOMENTS OF WILSON DISTRIBUTION OF  CENTRIC DATA
    AS COMPARED WITH THEORETICAL VALUES. (EXPECTED: 1.00)    
      #      RES        <I**2>/      <I**3>/      <I**4>/  
                         3<I>**2     15<I>**3    105<I>**4 

      22     3.512        0.526        0.203        0.062
      27     2.085        0.663        0.394        0.208
      29     1.638        0.643        0.357        0.172
      35     1.389        0.807        0.678        0.501
      35     1.229        0.502        0.195        0.064
      38     1.117        0.759        0.508        0.293
      42     1.028        0.675        0.470        0.318
      45     0.957        0.551        0.252        0.098
      49     0.897        0.563        0.290        0.139
      48     0.847        0.502        0.204        0.071
      48     0.807        0.557        0.256        0.100
      50     0.773        0.709        0.509        0.334
      54     0.742        0.598        0.309        0.139
      53     0.714        0.978        1.224        1.448
      62     0.689        0.557        0.249        0.094
      59     0.665        0.573        0.293        0.136
      58     0.645        0.524        0.228        0.087
      63     0.626        0.556        0.284        0.135
      55     0.610        0.736        0.579        0.421
     872   overall        0.629        0.396        0.260


 HIGHER ORDER MOMENTS OF WILSON DISTRIBUTION OF ACENTRIC DATA
    AS COMPARED WITH THEORETICAL VALUES. (EXPECTED: 1.00)    
      #      RES        <I**2>/      <I**3>/      <I**4>/  
                         2<I>**2      6<I>**3     24<I>**4 

       0   overall        0.000        0.000        0.000

   ======= CUMULATIVE INTENSITY DISTRIBUTION =======
 DEFINITIONS:
   <I>    = mean reflection intensity
 Na(Z)exp = expected number of acentric reflections with I <= Z*<I>
 Na(Z)obs = observed number of acentric reflections with I <= Z*<I>
 Nc(Z)exp = expected number of  centric reflections with I <= Z*<I>
 Nc(Z)obs = observed number of  centric reflections with I <= Z*<I>



 Nc(Z)obs/Nc(Z)exp versus resolution and Z (0.1-1.0)
      #      RES     0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0

      22     3.512  0.18  0.39  0.55  0.58  0.61  0.65  0.69  0.72  0.90  0.93
      27     2.085  0.45  0.54  0.53  0.70  0.78  0.73  0.68  0.65  0.79  0.87
      29     1.638  0.28  0.50  0.58  0.66  0.66  0.80  0.81  0.88  0.89  0.91
      35     1.389  0.12  0.17  0.34  0.72  0.93  0.92  0.91  0.95  0.96  0.96
      35     1.229  0.00  0.33  0.34  0.30  0.55  0.66  0.72  0.73  0.78  0.88
      38     1.117  0.11  0.30  0.76  1.00  0.91  0.98  1.06  1.09  1.08  1.04
      42     1.028  0.00  0.21  0.40  0.55  0.69  0.85  0.92  0.95  1.01  1.01
      45     0.957  0.00  0.06  0.32  0.52  0.73  0.75  0.78  0.81  0.88  0.94
      49     0.897  0.08  0.30  0.34  0.47  0.51  0.58  0.68  0.88  0.87  0.93
      48     0.847  0.08  0.06  0.15  0.22  0.36  0.63  0.73  0.80  0.98  0.95
      48     0.807  0.00  0.18  0.30  0.62  0.68  0.67  0.77  0.80  0.89  0.95
      50     0.773  0.08  0.12  0.48  0.55  0.61  0.78  0.84  0.92  1.04  1.03
      54     0.742  0.00  0.16  0.22  0.47  0.68  0.86  0.90  0.94  0.90  0.92
      53     0.714  0.15  0.16  0.45  0.72  0.83  0.97  1.04  1.02  1.01  1.02
      62     0.689  0.06  0.23  0.39  0.55  0.68  0.72  0.81  0.87  0.86  0.90
      59     0.665  0.00  0.10  0.20  0.36  0.62  0.85  0.88  0.94  0.90  0.94
      58     0.645  0.00  0.10  0.17  0.33  0.56  0.71  0.78  0.85  0.87  0.96
      63     0.626  0.06  0.18  0.19  0.30  0.46  0.54  0.69  0.88  0.97  1.00
      55     0.610  0.15  0.21  0.44  0.58  0.66  0.84  0.97  0.93  0.94  0.93
     872   overall  0.08  0.20  0.35  0.52  0.65  0.76  0.83  0.88  0.93  0.95


 Na(Z)obs/Na(Z)exp versus resolution and Z (0.1-1.0)
      #      RES     0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0

       0   overall  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00

 NUMBER OF UNIQUE ALIEN REFLECTIONS WITH A Z-SCORE ABOVE LIMIT         0
 (ALIENS ABOVE LIMIT (REJECT_ALIEN=      20.0) ARE MARKED INVALID)

 NUMBER OF REFLECTION RECORDS ON OUTPUT FILE "XDS_ASCII.HKL"       14373
 NUMBER OF ACCEPTED OBSERVATIONS (INCLUDING SYSTEMATIC ABSENCES)   14373
 NUMBER OF REJECTED MISFITS & ALIENS (marked by -1*SIGMA(IOBS))        0


 cpu time used                  0.3 sec
 elapsed wall-clock time        0.3 sec
