








class TestValues:
    def pool_size(cls, pool_size:int):
        if pool_size == None:
            assert type(cls._DEF_POOL_SIZE) is int and cls._DEF_POOL_SIZE>0, f"`{cls.__class__.__name__}._DEF_POOL_SIZE` should be an 'int' & greater than 0."

        elif type(pool_size) is int:
            assert pool_size>0 , "`pool_size` should be greater than 0."

        else:
            raise AssertionError("`pool_size` should be an 'int'.")



