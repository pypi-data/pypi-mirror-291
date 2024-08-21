from pytplot import sts_to_tplot, tnames, tplot
import pyspedas

if __name__ == "__main__":
    # Example of how to use this code
    # sts_to_tplot(sts_file='/path/to/your/sts_file.sts', read_only=False, prefix='', suffix='', merge=True, notplot=False)

    # v = pyspedas.maven.swea()
    # print(v)

    """

    f = [
        "/Users/nickhatzigeorgiu/data/maven/maven/data/sci/mag/l2/2015/01/mvn_mag_l2_2015002ss1s_20150102_v01_r01.sts",
        "/Users/nickhatzigeorgiu/data/maven/maven/data/sci/mag/l2/2015/01/mvn_mag_l2_2015001ss1s_20150101_v01_r01.sts",
    ]
    v = sts_to_tplot(
        filenames=f[0],  prefix="ttt_", suffix="_sss"
    )
    print(v)
    print(tnames())
    tplot(v)

    v1 = sts_to_tplot(
        filenames=f[1],  prefix="ttt_", suffix="_sss", merge=True
    )
    print(v1)
    print(tnames())
    tplot(v1)
    """
    kp_files = [
        "/Users/nickhatzigeorgiu/data//maven/maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160102_v20_r01.tab",
        "/Users/nickhatzigeorgiu/data//maven/maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160101_v20_r01.tab",
    ]

    kp_data_loaded = pyspedas.maven.maven_kp_to_tplot.maven_kp_to_tplot(
        filename=kp_files[0], ancillary_only=True, instruments="swe"
    )
    print(kp_data_loaded)
    
