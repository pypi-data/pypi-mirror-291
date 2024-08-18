"""委托接口"""

from vxutils import AbstractProvider, AbstractProviderCollection


class VXTdAPI(AbstractProviderCollection):
    """委托接口集合"""

    __defaults__ = {
        "current": {
            "mod_path": "vxquant.providers.tencenthq.VXTencentHQProvider",
            "params": {},
        },
    }
    __init__providers__ = [
        {"mod_path": "vxquant.providers.tencenthq.VXTencentHQInitProvider"}
    ]


if __name__ == "__main__":
    import time
    from vxutils import VXContext, loggerConfig

    loggerConfig()

    tdapi = VXTdAPI()
    print(tdapi._init_proviers)
    init_provider = tdapi._init_proviers[0]
    tdapi.start_up(init_provider)
    start = time.perf_counter()
    print(tdapi.current("600036.SH", "000001.SZ"))
    print("耗时: ", time.perf_counter() - start)
