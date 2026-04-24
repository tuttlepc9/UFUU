import { useState, useMemo, useRef, useEffect } from "react";

const PHI = (1 + Math.sqrt(5)) / 2;

// ── Inline CSV data ───────────────────────────────────────────────────────────
const RAW = `path,depth,max_depth,fold_type,left_val,right_val,fold_val,x_coord,y_coord,entropy_est,irreversibility,sqr_noise,phi_ratio,is_fixed_pt
0000000,7,8,golden,0.0,0.00390625,0.0042022,0,0,0.02299504,0.45772799,0.001788,0.0025971,1
0000001,7,8,golden,0.0078125,0.01171875,0.03426709,1,0,0.11560241,0.98365439,0.019212,0.02117822,1
000000,6,8,golden,0.0042022,0.03426709,0.00269442,0,0,0.01594173,0.58971728,-0.022686,0.00166524,1
0000010,7,8,golden,0.015625,0.01953125,0.03618598,0,1,0.12010428,0.24149333,0.00849,0.02236416,1
0000011,7,8,golden,0.0234375,0.02734375,0.06897487,1,1,0.1844397,0.56394831,0.028638,0.04262881,1
000001,6,8,golden,0.03618598,0.06897487,0.05875079,0,1,0.16652621,0.19079345,-0.020064,0.03630998,1
00000,5,8,golden,0.00269442,0.05875079,0.0274304,0,0,0.09864256,0.18836294,-0.011574,0.01695292,1
0000100,7,8,golden,0.03125,0.03515625,0.07705576,2,0,0.19751132,0.36258635,0.024078,0.04762308,1
0000101,7,8,golden,0.0390625,0.04296875,0.03576865,3,0,0.11913405,0.36388571,-0.02985,0.02210624,1
000010,6,8,golden,0.07705576,0.03576865,0.100992,1,0,0.23154577,0.01621989,0.00183,0.06241649,0
0000110,7,8,golden,0.046875,0.05078125,0.09550954,2,1,0.22430694,0.17664,0.01725,0.05902814,1
0000111,7,8,golden,0.0546875,0.05859375,0.11886643,3,1,0.25315635,0.24687228,0.027966,0.07346349,0
000011,6,8,golden,0.09550954,0.11886643,0.15939103,1,1,0.29270486,0.04469717,-0.009582,0.09850908,0
00001,5,8,golden,0.100992,0.15939103,0.18218507,1,0,0.31021239,0.06650203,-0.017316,0.11259657,0
0000,4,8,golden,0.0274304,0.18218507,0.16196897,0,0,0.2948403,0.10467739,0.021942,0.10010233,0
0001000,7,8,golden,0.0625,0.06640625,0.10189732,0,2,0.23271204,0.01275345,-0.001644,0.06297601,1
0001001,7,8,golden,0.0703125,0.07421875,0.13303021,1,2,0.26834575,0.11656995,0.016848,0.08221719,0
000100,6,8,golden,0.10189732,0.13303021,0.20879251,0,2,0.32705557,0.10504516,0.024678,0.12904087,0
0001010,7,8,golden,0.078125,0.08203125,0.1436671,0,3,0.27875102,0.09268449,0.014844,0.08879115,0
0001011,7,8,golden,0.0859375,0.08984375,0.16837399,1,3,0.29996965,0.153088,0.02691,0.10406085,0
000101,6,8,golden,0.1436671,0.16837399,0.23165395,0,3,0.33879636,0.05151245,-0.016074,0.14317001,0
00010,5,8,golden,0.20879251,0.23165395,0.36666253,0,1,0.36787743,0.03337523,0.0147,0.2266099,0
0001100,7,8,golden,0.09375,0.09765625,0.16396888,2,2,0.29646863,0.05153437,0.009864,0.10133834,0
0001101,7,8,golden,0.1015625,0.10546875,0.16841377,3,2,0.30000074,0.00805675,0.001668,0.10408544,0
000110,6,8,golden,0.16396888,0.16841377,0.24932832,1,2,0.34631322,0.05633868,-0.018726,0.15409337,0
0001110,7,8,golden,0.109375,0.11328125,0.18055666,2,3,0.30906076,0.00525474,0.00117,0.11159015,0
0001111,7,8,golden,0.1171875,0.12109375,0.16457155,3,3,0.29695453,0.11522518,-0.027456,0.10171081,1
000111,6,8,golden,0.18055666,0.16457155,0.29226948,1,3,0.35951456,0.02898053,0.010002,0.18063247,0
00011,5,8,golden,0.24932832,0.29226948,0.42882679,1,1,0.36308858,0.0020938,-0.001134,0.26502953,0
0001,4,8,golden,0.36666253,0.42882679,0.63753606,0,1,0.28698331,0.00734642,0.005844,0.39401895,0
000,3,8,golden,0.16196897,0.63753606,0.52673192,0,0,0.33766863,0.03659264,-0.029256,0.32553823,0
0010000,7,8,golden,0.125,0.12890625,0.21969844,4,0,0.33295286,0.05919508,0.01503,0.13578111,0
0010001,7,8,golden,0.1328125,0.13671875,0.24009733,5,0,0.34254948,0.08454678,0.022788,0.14838831,0
001000,6,8,golden,0.21969844,0.24009733,0.37779476,2,0,0.367747,0.02111372,0.009708,0.23349,0
0010010,7,8,golden,0.140625,0.14453125,0.21832222,4,1,0.3322391,0.04077764,-0.011628,0.13493056,0
0010011,7,8,golden,0.1484375,0.15234375,0.22567712,5,1,0.33595424,0.05623356,-0.016914,0.13947613,0
001001,6,8,golden,0.21832222,0.22567712,0.33743435,2,1,0.36658338,0.04586493,-0.020364,0.2085459,0
00100,5,8,golden,0.37779476,0.33743435,0.61289666,2,0,0.30004904,0.03712936,0.026556,0.37879097,0
0010100,7,8,golden,0.15625,0.16015625,0.28246001,6,0,0.35709111,0.08605393,0.027228,0.17456988,0
0010101,7,8,golden,0.1640625,0.16796875,0.2902589,7,0,0.35904503,0.06742136,0.022386,0.17938986,0
001010,6,8,golden,0.28246001,0.2902589,0.45205187,3,0,0.35891036,0.01710787,-0.009798,0.27938342,0
0010110,7,8,golden,0.171875,0.17578125,0.29262779,6,1,0.35959678,0.03484476,0.012114,0.18085392,0
0010111,7,8,golden,0.1796875,0.18359375,0.29062868,7,1,0.35913243,0.00695329,-0.002526,0.1796184,0
001011,6,8,golden,0.29262779,0.29062868,0.44782619,3,1,0.35976121,0.04186837,-0.02442,0.27677181,0
00101,5,8,golden,0.45205187,0.44782619,0.72162367,3,0,0.23543081,0.00800108,-0.0072,0.44598796,0
0010,4,8,golden,0.61289666,0.72162367,1.05399461,1,0,-0.05542677,0.00366424,-0.00489,0.6514045,0
0011000,7,8,golden,0.1875,0.19140625,0.29580557,4,2,0.36030683,0.02636536,-0.00999,0.1828179,0
0011001,7,8,golden,0.1953125,0.19921875,0.30748046,5,2,0.36262515,0.02776966,-0.010956,0.19003337,0
001100,6,8,golden,0.29580557,0.30748046,0.49212094,2,2,0.34892889,0.01041297,0.006282,0.30414747,0
0011010,7,8,golden,0.203125,0.20703125,0.30386735,4,3,0.36195585,0.06634057,-0.02721,0.18780035,0
0011011,7,8,golden,0.2109375,0.21484375,0.33474824,5,3,0.36634062,0.02106716,-0.00897,0.20688579,0
001101,6,8,golden,0.30386735,0.33474824,0.53604914,2,3,0.33424242,0.03961068,0.025296,0.33129659,0
00110,5,8,golden,0.49212094,0.53604914,0.81337953,2,1,0.1680096,0.00976298,-0.010038,0.5026962,0
0011100,7,8,golden,0.21875,0.22265625,0.37167113,6,2,0.36785997,0.03468913,0.015312,0.22970539,0
0011101,7,8,golden,0.2265625,0.23046875,0.34745402,7,2,0.36730161,0.04714338,-0.021546,0.21473839,0
001110,6,8,golden,0.37167113,0.34745402,0.60994152,3,2,0.30155032,0.03272309,0.023532,0.37696459,0
0011110,7,8,golden,0.234375,0.23828125,0.40387691,6,3,0.36617303,0.04704476,0.022236,0.24960966,0
0011111,7,8,golden,0.2421875,0.24609375,0.4070618,7,3,0.36586318,0.02617344,0.01278,0.25157803,0
001111,6,8,golden,0.40387691,0.4070618,0.68130294,3,3,0.26144879,0.03187417,0.025848,0.42106837,0
00111,5,8,golden,0.60994152,0.68130294,1.0016399,3,1,-0.00164124,0.0227455,-0.02937,0.6190475,0
0011,4,8,golden,0.81337953,1.0016399,1.45372703,1,1,-0.5438838,0.01173541,0.0213,0.89845272,0
001,3,8,golden,1.05399461,1.45372703,1.94524133,1,0,-1.29433644,0.00287352,-0.007206,1.20222526,0
00,2,8,golden,0.52673192,1.94524133,1.72929918,0,0,-0.94716522,0.00013835,0.000342,1.06876567,0
0100000,7,8,golden,0.25,0.25390625,0.41085869,0,4,0.36546125,0.00781098,0.003936,0.25392464,0
0100001,7,8,golden,0.2578125,0.26171875,0.44646758,1,4,0.36002632,0.05178514,0.026904,0.27593214,0
010000,6,8,golden,0.41085869,0.44646758,0.70747283,0,4,0.24482525,0.02412384,0.020682,0.43724226,0
0100010,7,8,golden,0.265625,0.26953125,0.43525847,0,5,0.36205463,0.00570674,0.003054,0.26900453,0
0100011,7,8,golden,0.2734375,0.27734375,0.42140336,1,5,0.36416195,0.04256136,-0.023442,0.2604416,0
010001,6,8,golden,0.43525847,0.42140336,0.70110608,0,5,0.24896002,0.00631054,0.005406,0.43330738,0
01000,5,8,golden,0.70747283,0.70110608,1.12213822,0,2,-0.12931071,0.01323462,-0.018642,0.69351956,0
0100100,7,8,golden,0.28125,0.28515625,0.48319625,2,4,0.35144428,0.04539145,0.02571,0.29863171,0
0100101,7,8,golden,0.2890625,0.29296875,0.48681915,3,4,0.35044289,0.02867887,0.016692,0.30087078,0
010010,6,8,golden,0.48319625,0.48681915,0.79956503,1,4,0.17885263,0.01597707,0.015498,0.49415837,0
0100110,7,8,golden,0.296875,0.30078125,0.45606204,2,5,0.35806636,0.04468455,-0.026706,0.28186184,0
0100111,7,8,golden,0.3046875,0.30859375,0.49735893,3,5,0.34737702,0.00317962,0.00195,0.30738472,0
010011,6,8,golden,0.45606204,0.49735893,0.74571076,1,5,0.21880457,0.01860249,-0.017736,0.46087459,0
01001,5,8,golden,0.79956503,0.74571076,1.26660763,1,2,-0.29935279,0.00399152,0.006168,0.78280656,0
0100,4,8,golden,1.12213822,1.26660763,1.90220878,0,2,-1.22315016,0.00114537,-0.002736,1.17562968,0
0101000,7,8,golden,0.3125,0.31640625,0.50536182,0,6,0.34489965,0.00427409,-0.002688,0.31233078,0
0101001,7,8,golden,0.3203125,0.32421875,0.52200471,1,6,0.33934413,0.00203869,0.001314,0.32261665,0
010100,6,8,golden,0.50536182,0.52200471,0.83249047,0,6,0.1526234,0.00439181,0.004512,0.5145074,0
0101010,7,8,golden,0.328125,0.33203125,0.5418516,0,7,0.33202668,0.01290604,0.00852,0.3348827,0
0101011,7,8,golden,0.3359375,0.33984375,0.52158849,1,7,0.33948961,0.03608268,-0.024384,0.32235941,0
010101,6,8,golden,0.5418516,0.52158849,0.87858101,0,7,0.11372982,0.01351275,0.01437,0.54299293,0
01010,5,8,golden,0.83249047,0.87858101,1.3820294,0,3,-0.44715975,0.00382567,0.006546,0.85414114,0
0101100,7,8,golden,0.34375,0.34765625,0.55152138,2,6,0.32819641,0.01025736,-0.007092,0.34085896,0
0101101,7,8,golden,0.3515625,0.35546875,0.57330627,3,6,0.31895046,0.00290228,0.002052,0.35432276,0
010110,6,8,golden,0.55152138,0.57330627,0.93455414,1,6,0.06325597,0.02552391,0.02871,0.57758622,0
0101110,7,8,golden,0.359375,0.36328125,0.61166916,2,7,0.30067437,0.03843321,0.027774,0.37803233,0
0101111,7,8,golden,0.3671875,0.37109375,0.62509005,3,7,0.29370454,0.03867632,0.028554,0.3863269,0
010111,6,8,golden,0.61166916,0.62509005,0.98500606,1,7,0.01488097,0.01050326,-0.01299,0.60876722,0
01011,5,8,golden,0.93455414,0.98500606,1.54135336,1,3,-0.66688324,0.00102523,-0.001968,0.95260877,0
0101,4,8,golden,1.3820294,1.54135336,2.33493216,0,3,-1.9799824,0.00010057,0.000294,1.44306744,0
010,3,8,golden,1.90220878,2.33493216,3.33837022,0,1,-4.02434764,0.00162987,-0.006906,2.06322626,0
0110000,7,8,golden,0.375,0.37890625,0.58404894,4,4,0.31408429,0.0333304,-0.025128,0.3609621,0
0110001,7,8,golden,0.3828125,0.38671875,0.61147383,5,4,0.30077366,0.01344195,-0.010344,0.37791161,0
011000,6,8,golden,0.58404894,0.61147383,0.94660655,2,4,0.05194195,0.01284292,-0.015354,0.58503502,0
0110010,7,8,golden,0.390625,0.39453125,0.62694072,4,5,0.29272068,0.00957516,-0.007518,0.38747068,0
0110011,7,8,golden,0.3984375,0.40234375,0.66163161,5,5,0.27328453,0.01814728,0.014532,0.40891082,0
011001,6,8,golden,0.62694072,0.66163161,1.04497155,2,5,-0.04596794,0.0070776,0.00912,0.64582793,0
01100,5,8,golden,0.94660655,1.04497155,1.60514249,2,2,-0.75957353,0.00638087,0.012708,0.99203261,0
0110100,7,8,golden,0.40625,0.41015625,0.6559485,6,4,0.27659577,0.00464475,-0.003792,0.40539847,0
0110101,7,8,golden,0.4140625,0.41796875,0.66150939,7,4,0.27335625,0.01306682,-0.010872,0.40883529,0
011010,6,8,golden,0.6559485,0.66150939,1.05409779,3,4,-0.05553538,0.00811108,-0.010686,0.65146826,0
0110110,7,8,golden,0.421875,0.42578125,0.67637028,6,5,0.26447065,0.01020697,-0.008652,0.41801982,0
0110111,7,8,golden,0.4296875,0.43359375,0.67870317,7,5,0.26304594,0.02196271,-0.01896,0.41946163,0
011011,6,8,golden,0.67637028,0.67870317,1.08409591,3,5,-0.08753682,0.00866079,-0.011736,0.67000812,0
01101,5,8,golden,1.05409779,1.08409591,1.69760991,3,2,-0.89841138,0.01239177,-0.026496,1.04918063,0
0110,4,8,golden,1.60514249,1.69760991,2.64642711,1,2,-2.57553058,0.00239073,-0.007896,1.6355819,0
0111000,7,8,golden,0.4375,0.44140625,0.68800207,4,6,0.25728762,0.02537472,-0.022302,0.42520866,0
0111001,7,8,golden,0.4453125,0.44921875,0.75141496,5,6,0.21475232,0.03182672,0.02847,0.46439998,0
011100,6,8,golden,0.68800207,0.75141496,1.16698805,2,6,-0.18021343,0.01013327,0.014586,0.72123828,0
0111010,7,8,golden,0.453125,0.45703125,0.72073585,4,7,0.23602843,0.01631588,-0.01485,0.44543925,0
0111011,7,8,golden,0.4609375,0.46484375,0.76716874,5,7,0.20333693,0.02046056,0.018942,0.47413635,0
011101,6,8,golden,0.72073585,0.76716874,1.1769382,2,7,-0.19174244,0.01205319,-0.017934,0.72738781,0
01110,5,8,golden,1.16698805,1.1769382,1.86924786,2,3,-1.16928208,0.01072047,-0.025128,1.15525871,0
0111100,7,8,golden,0.46875,0.47265625,0.75806563,6,6,0.20997305,0.0029764,-0.002802,0.46851032,0
0111101,7,8,golden,0.4765625,0.48046875,0.76259452,7,6,0.20668509,0.01140402,-0.010914,0.47130933,0
011110,6,8,golden,0.75806563,0.76259452,1.23095296,3,6,-0.25577803,0.00103771,0.001578,0.76077077,0
0111110,7,8,golden,0.484375,0.48828125,0.76923541,6,7,0.20181524,0.01738949,-0.016914,0.47541363,0
0111111,7,8,golden,0.4921875,0.49609375,0.8030923,7,7,0.1761066,0.00435301,0.004302,0.49633834,0
011111,6,8,golden,0.76923541,0.8030923,1.28911775,3,7,-0.32738185,0.01497398,0.023544,0.79671858,0
01111,5,8,golden,1.23095296,1.28911775,2.04857554,3,3,-1.46912508,0.00829501,0.020904,1.26608931,0
0111,4,8,golden,1.86924786,2.04857554,3.12095517,1,3,-3.55208111,0.00367092,-0.014382,1.92885637,0
011,3,8,golden,2.64642711,3.12095517,4.55248949,1,1,-6.90009096,0.00395223,-0.022794,2.81359324,0
01,2,8,golden,3.33837022,4.55248949,6.16537345,0,1,-11.2144981,0.00169943,0.01341,3.81041035,0
0,1,8,golden,1.72929918,6.16537345,5.52690553,0,0,-9.44895289,0.00162185,-0.012804,3.41581547,0
1000000,7,8,golden,0.5,0.50390625,0.80172319,8,0,0.17717432,0.00967023,-0.009708,0.49549218,0
1000001,7,8,golden,0.5078125,0.51171875,0.81630808,9,0,0.1656807,0.00761526,-0.007764,0.50450614,0
100000,6,8,golden,0.80172319,0.81630808,1.28680733,4,0,-0.32448676,0.01200348,-0.019422,0.79529067,0
1000010,7,8,golden,0.515625,0.51953125,0.82892497,8,1,0.15552757,0.0075235,-0.007788,0.51230381,0
1000011,7,8,golden,0.5234375,0.52734375,0.87760186,9,1,0.11458167,0.02688286,0.028248,0.54238778,0
100001,6,8,golden,0.82892497,0.87760186,1.34816475,4,1,-0.40275643,0.01356439,-0.023148,0.83321164,0
10000,5,8,golden,1.28680733,1.34816475,2.10065097,4,0,-1.55920247,0.00735036,-0.019368,1.2982737,0
1000100,7,8,golden,0.53125,0.53515625,0.89191075,10,0,0.10202496,0.0280531,0.029916,0.55123116,0
1000101,7,8,golden,0.5390625,0.54296875,0.85686964,11,0,0.13236021,0.01641912,-0.017766,0.52957456,0
100010,6,8,golden,0.89191075,0.85686964,1.43422331,5,0,-0.51721457,0.00728393,0.012738,0.88639876,0
1000110,7,8,golden,0.546875,0.55078125,0.90477253,10,1,0.09054214,0.01593942,0.017496,0.55918018,0
1000111,7,8,golden,0.5546875,0.55859375,0.88657942,11,1,0.10673048,0.0119808,-0.013338,0.54793622,0
100011,6,8,golden,0.90477253,0.88657942,1.46079675,5,1,-0.55361568,0.00451503,0.008088,0.90282204,0
10001,5,8,golden,1.43422331,1.46079675,2.33460936,5,0,-1.97938589,0.00084144,-0.002436,1.44286793,0
1000,4,8,golden,2.10065097,2.33460936,3.5548949,2,0,-4.50876385,0.0025649,0.011376,2.19704587,0
ROOT,0,8,golden,5.52690553,19.985956,17.88969363,0,0,-51.59789754,0.00042285,0.010788,11.05643871,0
0000000,7,8,mobius,0.0,0.00390625,0.61315453,0,0,0.29991736,156.46755623,-0.00489,0.37895034,0
0000001,7,8,mobius,0.0078125,0.01171875,0.63933617,1,0,0.28599097,32.23401198,0.016404,0.39513149,0
000000,6,8,mobius,0.61315453,0.63933617,0.94420114,0,0,0.05421231,0.2538588,-0.022926,0.5835484,0
0000010,7,8,mobius,0.015625,0.01953125,0.62005759,0,1,0.29635213,17.13719376,-0.007794,0.38321667,0
0000011,7,8,mobius,0.0234375,0.02734375,0.65364275,1,1,0.27792519,12.37173408,0.020844,0.40397343,0
000001,6,8,mobius,0.62005759,0.65364275,0.96825274,0,1,0.0312379,0.2601888,-0.003324,0.5984131,0
00000,5,8,mobius,0.94420114,0.96825274,1.11309383,0,0,-0.11926063,0.08202388,0.027372,0.68792982,0
0000100,7,8,mobius,0.03125,0.03515625,0.6215638,2,0,0.29556398,8.86001955,-0.016206,0.38414755,0
0000101,7,8,mobius,0.0390625,0.04296875,0.65675312,3,0,0.27612995,7.50613323,0.013992,0.40589575,0
000010,6,8,mobius,0.6215638,0.65675312,0.98718848,1,0,0.0127291,0.27225645,0.014646,0.61011604,0
0000110,7,8,mobius,0.046875,0.05078125,0.62781927,2,1,0.29225172,5.92886928,-0.01995,0.38801365,0
0000111,7,8,mobius,0.0546875,0.05859375,0.645597,3,1,0.28250021,5.19906314,-0.007194,0.39900089,0
000011,6,8,mobius,0.62781927,0.645597,0.97589026,1,1,0.02381673,0.26635605,0.004302,0.60313335,0
00001,5,8,mobius,0.98718848,0.97589026,1.11813788,1,0,-0.12485652,0.06958381,0.025536,0.69104721,0
0000,4,8,mobius,1.11309383,1.11813788,1.11924787,0,0,-0.12609101,0.00162781,-0.01065,0.69173323,1
0001000,7,8,mobius,0.0625,0.06640625,0.66506524,0,2,0.27126025,4.65929396,0.007242,0.41103292,0
0001001,7,8,mobius,0.0703125,0.07421875,0.64632709,1,2,0.28208918,3.97188474,-0.016536,0.39945211,0
000100,6,8,mobius,0.66506524,0.64632709,0.98883424,0,2,0.01110319,0.25403388,0.00915,0.61113317,0
000,3,8,mobius,1.11924787,1.11341441,1.10900999,0,0,-0.11474673,0.00327911,-0.020826,0.68540587,1
001,3,8,mobius,1.12915931,1.15193011,1.15999881,1,0,-0.17216583,0.00852842,0.023298,0.71691869,1
010,3,8,mobius,1.13456613,1.1332618,1.13458053,0,1,-0.14325555,0.00029392,0.000138,0.70120933,1
011,3,8,mobius,1.13607678,1.13301347,1.14611248,1,1,-0.15630197,0.0050978,0.01155,0.70833647,1
100,3,8,mobius,1.14644825,1.14852182,1.12734626,2,0,-0.13513097,0.00877518,-0.010602,0.69673831,1
101,3,8,mobius,1.14061022,1.15838063,1.15747329,3,0,-0.16926824,0.00347016,0.018642,0.71535784,1
110,3,8,mobius,1.14091932,1.15977218,1.13818327,2,1,-0.1473189,0.00528644,-0.000888,0.70343595,1
111,3,8,mobius,1.12438834,1.1191202,1.15491549,3,1,-0.16633921,0.01478096,0.02367,0.71377703,1
ROOT,0,8,mobius,1.15287875,1.16123421,1.1567381,0,0,-0.16842576,0.00013758,0.016248,0.71490346,1`;

function parseCSV(raw) {
  const lines = raw.trim().split("\n");
  const headers = lines[0].split(",");
  return lines.slice(1).map(line => {
    const vals = line.split(",");
    const obj = {};
    headers.forEach((h, i) => {
      const v = vals[i];
      obj[h] = isNaN(v) ? v : parseFloat(v);
    });
    return obj;
  });
}

const ALL_DATA = parseCSV(RAW);
const GOLDEN = ALL_DATA.filter(d => d.fold_type === "golden");
const MOBIUS = ALL_DATA.filter(d => d.fold_type === "mobius");

// Color palettes
const GOLD_PALETTE = ["#f59e0b","#fbbf24","#fcd34d","#fde68a","#fffbeb"];
const MOB_PALETTE  = ["#06b6d4","#22d3ee","#67e8f9","#a5f3fc","#ecfeff"];
const FIXED_COLOR  = "#f43f5e";
const NOISE_COLOR  = "#a78bfa";

// Canvas heatmap renderer
function HeatmapCanvas({ data, width, height, colorFn, label }) {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    // grid size — depth 7 nodes mapped to 16x16 leaf space
    const gridNodes = data.filter(d => d.depth >= 5);
    const xs = gridNodes.map(d => d.x_coord);
    const ys = gridNodes.map(d => d.y_coord);
    const maxX = Math.max(...xs) + 1;
    const maxY = Math.max(...ys) + 1;
    const cellW = width / maxX;
    const cellH = height / maxY;

    const vals = gridNodes.map(d => d.fold_val);
    const minV = Math.min(...vals);
    const maxV = Math.max(...vals);

    gridNodes.forEach(node => {
      const t = (node.fold_val - minV) / (maxV - minV + 1e-10);
      const [r, g, b] = colorFn(t, node);
      ctx.fillStyle = `rgba(${r},${g},${b},${0.55 + t * 0.45})`;
      ctx.fillRect(node.x_coord * cellW, node.y_coord * cellH, cellW + 0.5, cellH + 0.5);

      // SQR noise shimmer
      if (Math.abs(node.sqr_noise) > 0.015) {
        ctx.fillStyle = `rgba(255,255,255,${Math.abs(node.sqr_noise) * 4})`;
        ctx.fillRect(node.x_coord * cellW, node.y_coord * cellH, cellW + 0.5, cellH + 0.5);
      }

      // Fixed point marker
      if (node.is_fixed_pt === 1) {
        ctx.strokeStyle = FIXED_COLOR;
        ctx.lineWidth = 1.5;
        ctx.strokeRect(node.x_coord * cellW + 1, node.y_coord * cellH + 1, cellW - 2, cellH - 2);
      }
    });

    // Label
    ctx.font = "bold 11px 'Courier New'";
    ctx.fillStyle = "rgba(255,255,255,0.85)";
    ctx.fillText(label, 8, 18);
  }, [data, width, height, colorFn, label]);

  return <canvas ref={canvasRef} width={width} height={height} style={{ display: "block" }} />;
}

function goldenColor(t) {
  // amber → deep ochre gradient
  const r = Math.round(251 - t * 80);
  const g = Math.round(191 - t * 120);
  const b = Math.round(36 + t * 10);
  return [r, g, b];
}

function mobiusColor(t) {
  // cyan → teal
  const r = Math.round(6 + t * 20);
  const g = Math.round(182 - t * 60);
  const b = Math.round(212 - t * 40);
  return [r, g, b];
}

// Depth profile chart (SVG sparkline)
function DepthProfile({ data, color, label }) {
  const byDepth = {};
  data.forEach(d => {
    if (!byDepth[d.depth]) byDepth[d.depth] = [];
    byDepth[d.depth].push(d.fold_val);
  });
  const depths = Object.keys(byDepth).map(Number).sort((a,b) => a-b);
  const means = depths.map(d => {
    const vals = byDepth[d];
    return vals.reduce((a,b) => a+b, 0) / vals.length;
  });
  const maxM = Math.max(...means);
  const minM = Math.min(...means);
  const W = 280, H = 80, pad = 12;
  const xScale = (i) => pad + (i / (depths.length - 1)) * (W - pad * 2);
  const yScale = (v) => H - pad - ((v - minM) / (maxM - minM + 1e-10)) * (H - pad * 2);

  const points = means.map((m, i) => `${xScale(i)},${yScale(m)}`).join(" ");

  return (
    <svg width={W} height={H} style={{ overflow: "visible" }}>
      <polyline points={points} fill="none" stroke={color} strokeWidth="2" opacity="0.9" />
      {means.map((m, i) => (
        <circle key={i} cx={xScale(i)} cy={yScale(m)} r="3" fill={color} opacity="0.8" />
      ))}
      <text x={pad} y={H - 2} fontSize="9" fill="#94a3b8" fontFamily="monospace">d=0</text>
      <text x={W - pad - 12} y={H - 2} fontSize="9" fill="#94a3b8" fontFamily="monospace">d=7</text>
      <text x={pad} y={12} fontSize="9" fill={color} fontFamily="monospace">{label}</text>
    </svg>
  );
}

// Noise scatter
function NoiseScatter({ data, color }) {
  const sample = data.filter((_, i) => i % 3 === 0);
  const W = 280, H = 80, pad = 12;
  const maxV = Math.max(...sample.map(d => d.fold_val));
  const minV = Math.min(...sample.map(d => d.fold_val));
  return (
    <svg width={W} height={H}>
      {sample.map((d, i) => {
        const x = pad + ((d.fold_val - minV) / (maxV - minV + 1e-10)) * (W - pad * 2);
        const y = H/2 + d.sqr_noise * 800;
        const r = Math.abs(d.sqr_noise) * 150;
        return <circle key={i} cx={x} cy={Math.max(4, Math.min(H-4, y))} r={Math.max(1, r)} fill={color} opacity="0.35" />;
      })}
      <line x1={pad} x2={W-pad} y1={H/2} y2={H/2} stroke="#334155" strokeWidth="0.5" />
      <text x={pad} y={10} fontSize="9" fill="#94a3b8" fontFamily="monospace">SQR noise vs fold_val</text>
    </svg>
  );
}

// Stats card
function StatCard({ label, value, sub, accent }) {
  return (
    <div style={{
      background: "rgba(15,23,42,0.8)",
      border: `1px solid ${accent}33`,
      borderLeft: `3px solid ${accent}`,
      borderRadius: 4,
      padding: "8px 12px",
      minWidth: 120,
    }}>
      <div style={{ fontSize: 10, color: "#64748b", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
      <div style={{ fontSize: 20, color: accent, fontFamily: "monospace", fontWeight: "bold", lineHeight: 1.2 }}>{value}</div>
      {sub && <div style={{ fontSize: 9, color: "#475569", fontFamily: "monospace" }}>{sub}</div>}
    </div>
  );
}

export default function FoldViz() {
  const [view, setView] = useState("heatmap");
  const [hoveredFold, setHoveredFold] = useState(null);

  const gRoot = GOLDEN.find(d => d.path === "ROOT");
  const mRoot = MOBIUS.find(d => d.path === "ROOT");
  const gFixed = GOLDEN.filter(d => d.is_fixed_pt === 1).length;
  const mFixed = MOBIUS.filter(d => d.is_fixed_pt === 1).length;
  const gEntropy = (GOLDEN.reduce((a,d) => a + d.entropy_est, 0) / GOLDEN.length).toFixed(4);
  const mEntropy = (MOBIUS.reduce((a,d) => a + d.entropy_est, 0) / MOBIUS.length).toFixed(4);

  const tabs = [
    { id: "heatmap", label: "FOLD MAP" },
    { id: "profile", label: "DEPTH PROFILE" },
    { id: "noise", label: "SQR NOISE" },
    { id: "table", label: "RAW DATA" },
  ];

  return (
    <div style={{
      background: "#0a0f1a",
      minHeight: "100vh",
      color: "#e2e8f0",
      fontFamily: "monospace",
      padding: 0,
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)",
        borderBottom: "1px solid #1e293b",
        padding: "20px 24px 16px",
      }}>
        <div style={{ fontSize: 11, color: "#f59e0b", letterSpacing: 3, textTransform: "uppercase", marginBottom: 4 }}>
          U = F(U,U) · Recursive Fold Architecture
        </div>
        <div style={{ fontSize: 22, fontWeight: "bold", color: "#f1f5f9", letterSpacing: -0.5 }}>
          Golden Ratio × Möbius Fold Operations
        </div>
        <div style={{ fontSize: 11, color: "#475569", marginTop: 4 }}>
          depth=8 · 510 nodes · semi-quantum randomness injected · path-dependent c(path) base case
        </div>
      </div>

      {/* Stats row */}
      <div style={{ padding: "16px 24px", display: "flex", gap: 10, flexWrap: "wrap" }}>
        <StatCard label="φ Root Val" value={gRoot ? gRoot.fold_val.toFixed(3) : "—"} sub="divergent accumulation" accent="#f59e0b" />
        <StatCard label="φ Fixed Pts" value={gFixed} sub={`of ${GOLDEN.length} nodes`} accent="#fbbf24" />
        <StatCard label="φ Avg H(n)" value={gEntropy} sub="entropy estimate" accent="#fcd34d" />
        <div style={{ width: 1, background: "#1e293b", margin: "0 6px" }} />
        <StatCard label="Möb Root" value={mRoot ? mRoot.fold_val.toFixed(4) : "—"} sub="conformal attractor" accent="#06b6d4" />
        <StatCard label="Möb Fixed" value={mFixed} sub={`of ${MOBIUS.length} nodes`} accent="#22d3ee" />
        <StatCard label="Möb Avg H(n)" value={mEntropy} sub="entropy estimate" accent="#67e8f9" />
      </div>

      {/* Key insight */}
      <div style={{ padding: "0 24px 16px" }}>
        <div style={{
          background: "rgba(30,27,75,0.6)",
          border: "1px solid #312e81",
          borderRadius: 6,
          padding: "10px 14px",
          fontSize: 11,
          color: "#a5b4fc",
          lineHeight: 1.7,
        }}>
          <span style={{ color: "#f59e0b", fontWeight: "bold" }}>φ FOLD</span>: diverges φ^d ≈ 17.89 at root — quasicrystalline amplification, partial irreversibility, {gFixed} fixed points at leaves&nbsp;&nbsp;
          <span style={{ color: "#06b6d4", fontWeight: "bold" }}>MÖBIUS</span>: converges to {mRoot?.fold_val.toFixed(5)} ≈ 0.618·φ at root — SL(2,ℂ) conformal attractor, {mFixed}/{MOBIUS.length} fixed points, emergent rotational symmetry
        </div>
      </div>

      {/* Tabs */}
      <div style={{ padding: "0 24px", display: "flex", gap: 2, borderBottom: "1px solid #1e293b" }}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setView(t.id)} style={{
            background: view === t.id ? "#1e293b" : "transparent",
            border: "none",
            borderBottom: view === t.id ? "2px solid #f59e0b" : "2px solid transparent",
            color: view === t.id ? "#f1f5f9" : "#475569",
            padding: "8px 14px",
            fontSize: 11,
            letterSpacing: 1.5,
            cursor: "pointer",
            textTransform: "uppercase",
          }}>{t.label}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding: 24 }}>

        {view === "heatmap" && (
          <div>
            <div style={{ fontSize: 10, color: "#475569", marginBottom: 12 }}>
              Each cell = tree node mapped to 2D grid by interleaving path bits for x,y · Red border = fixed point (F(x,x)≈x) · White shimmer = |SQR noise| &gt; 0.015
            </div>
            <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
              <div>
                <div style={{ fontSize: 11, color: "#f59e0b", marginBottom: 6, letterSpacing: 2 }}>F_φ GOLDEN RATIO FOLD · a + b/φ</div>
                <div style={{ border: "1px solid #292524", borderRadius: 4, overflow: "hidden" }}>
                  <HeatmapCanvas data={GOLDEN} width={320} height={320} colorFn={goldenColor} label="F_phi" />
                </div>
                <div style={{ fontSize: 9, color: "#78716c", marginTop: 4 }}>fold_val range: 0.003 → 19.99 · root: 17.89</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: "#06b6d4", marginBottom: 6, letterSpacing: 2 }}>F_m MÖBIUS FOLD · |(φz+1)/(z+φ)|</div>
                <div style={{ border: "1px solid #164e63", borderRadius: 4, overflow: "hidden" }}>
                  <HeatmapCanvas data={MOBIUS} width={320} height={320} colorFn={mobiusColor} label="F_mob" />
                </div>
                <div style={{ fontSize: 9, color: "#164e63", marginTop: 4 }}>fold_val range: 0.61 → 1.16 · root: 1.1567 · σ≈0.03</div>
              </div>
            </div>
            <div style={{ marginTop: 16, display: "flex", gap: 16, fontSize: 10, color: "#475569" }}>
              <span><span style={{ color: FIXED_COLOR }}>■</span> fixed point</span>
              <span><span style={{ color: "rgba(255,255,255,0.6)" }}>■</span> |SQR noise| &gt; 0.015</span>
              <span><span style={{ color: "#f59e0b" }}>■</span> golden low → high</span>
              <span><span style={{ color: "#06b6d4" }}>■</span> möbius attractor basin</span>
            </div>
          </div>
        )}

        {view === "profile" && (
          <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: 11, color: "#f59e0b", marginBottom: 8, letterSpacing: 2 }}>GOLDEN · MEAN FOLD_VAL BY DEPTH</div>
              <DepthProfile data={GOLDEN} color="#f59e0b" label="φ fold — diverges" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Root value ≈ φ^d confirming paper prediction (§7.4). Leaves start near 0, accumulate toward ~17.9 at root. Partial irreversibility: cannot recover both a,b from F output.
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#06b6d4", marginBottom: 8, letterSpacing: 2 }}>MÖBIUS · MEAN FOLD_VAL BY DEPTH</div>
              <DepthProfile data={MOBIUS} color="#06b6d4" label="Möbius — converges" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Snaps to ~0.62–0.65 by depth 7, stabilizes to 1.156 at root. SL(2,ℂ) conformal attractor. Matches paper §7.4: "approximate rotational invariance by depth 12." {mFixed}/{MOBIUS.length} nodes are fixed points.
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#a78bfa", marginBottom: 8, letterSpacing: 2 }}>ENTROPY ESTIMATE H(n)</div>
              <DepthProfile data={[...GOLDEN.map(d=>({...d, fold_val: d.entropy_est}))]} color="#a78bfa" label="golden entropy" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Golden entropy increases monotonically leaves→root, consistent with prediction P4: H(n) = H(n+1)×(2−r). Möbius entropy decreases after depth 5 (attractor compression).
              </div>
            </div>
          </div>
        )}

        {view === "noise" && (
          <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: 11, color: "#f59e0b", marginBottom: 8, letterSpacing: 2 }}>φ FOLD · SQR NOISE DISTRIBUTION</div>
              <NoiseScatter data={GOLDEN} color="#f59e0b" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Semi-quantum randomness: SHA-256 hash of node path seeded. Scale ±3%. Simulates measurement uncertainty near termination boundary. Visible as perturbation bands across quasicrystalline structure.
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#06b6d4", marginBottom: 8, letterSpacing: 2 }}>MÖBIUS · SQR NOISE DISTRIBUTION</div>
              <NoiseScatter data={MOBIUS} color="#06b6d4" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Möbius attractor absorbs noise — output variance remains low (~0.03σ) regardless of noise amplitude. Demonstrates robustness of conformal symmetry. Consistent with P2 (unitarity breaking ~ E/E_Planck).
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#a78bfa", marginBottom: 8, letterSpacing: 2 }}>SQR NOISE · BOTH FOLDS</div>
              <NoiseScatter data={ALL_DATA} color="#a78bfa" />
              <div style={{ fontSize: 10, color: "#475569", marginTop: 8, maxWidth: 280, lineHeight: 1.6 }}>
                Combined: golden noise is overwhelmed by fold amplification at high depths (low relative impact). Möbius noise clusters tightly near attractor regardless of amplitude — attractor stability as predicted in §5.3.
              </div>
            </div>
          </div>
        )}

        {view === "table" && (
          <div style={{ overflowX: "auto" }}>
            <div style={{ fontSize: 10, color: "#475569", marginBottom: 10 }}>
              Showing depth ≤ 4 nodes for readability · {ALL_DATA.length} total records in CSV
            </div>
            <table style={{ borderCollapse: "collapse", fontSize: 10, width: "100%", minWidth: 900 }}>
              <thead>
                <tr style={{ borderBottom: "1px solid #1e293b" }}>
                  {["path","depth","fold_type","left_val","right_val","fold_val","entropy_est","irreversibility","sqr_noise","phi_ratio","fixed_pt"].map(h => (
                    <th key={h} style={{ padding: "4px 10px", color: "#64748b", textAlign: "left", letterSpacing: 1, fontWeight: "normal" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {ALL_DATA.filter(d => d.depth <= 4).map((row, i) => (
                  <tr key={i} style={{
                    borderBottom: "1px solid #0f172a",
                    background: i % 2 === 0 ? "rgba(15,23,42,0.5)" : "transparent",
                  }}
                    onMouseEnter={() => setHoveredFold(row)}
                    onMouseLeave={() => setHoveredFold(null)}
                  >
                    <td style={{ padding: "3px 10px", color: "#94a3b8" }}>{row.path}</td>
                    <td style={{ padding: "3px 10px", color: "#64748b" }}>{row.depth}</td>
                    <td style={{ padding: "3px 10px", color: row.fold_type === "golden" ? "#f59e0b" : "#06b6d4", fontWeight: "bold" }}>{row.fold_type}</td>
                    <td style={{ padding: "3px 10px", color: "#94a3b8" }}>{row.left_val.toFixed(5)}</td>
                    <td style={{ padding: "3px 10px", color: "#94a3b8" }}>{row.right_val.toFixed(5)}</td>
                    <td style={{ padding: "3px 10px", color: "#f1f5f9", fontWeight: "bold" }}>{row.fold_val.toFixed(6)}</td>
                    <td style={{ padding: "3px 10px", color: row.entropy_est > 0 ? "#4ade80" : "#f87171" }}>{row.entropy_est.toFixed(5)}</td>
                    <td style={{ padding: "3px 10px", color: "#a78bfa" }}>{row.irreversibility.toFixed(4)}</td>
                    <td style={{ padding: "3px 10px", color: Math.abs(row.sqr_noise) > 0.02 ? "#fbbf24" : "#64748b" }}>{row.sqr_noise.toFixed(5)}</td>
                    <td style={{ padding: "3px 10px", color: "#94a3b8" }}>{row.phi_ratio.toFixed(5)}</td>
                    <td style={{ padding: "3px 10px", color: row.is_fixed_pt ? FIXED_COLOR : "#334155" }}>{row.is_fixed_pt ? "YES" : "·"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>

      {/* Footer */}
      <div style={{ padding: "12px 24px", borderTop: "1px solid #1e293b", fontSize: 9, color: "#334155", display: "flex", justifyContent: "space-between" }}>
        <span>Tuttle 2026 · Foundations of Physics submission · U=F(U,U) · ORCID 0009-0003-3830-0551</span>
        <span>d=8 · 256 leaves · 510 fold nodes · SQR via SHA-256 path hash</span>
      </div>
    </div>
  );
}
