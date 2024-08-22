import os
import typing

from stuff_saver.utils import hasher, mkdir_p


class StuffSaver:
    """StuffSaver class to save and reload data from a temporary folder

    Attributes:
        path (str): Path to the temporary folder where the data will be saved.
        backend (_type_): Backend to use for saving the data. It should have the methods load and dump.

    Methods:
        exists(request_key: typing.Hashable) -> bool: Check if the data exists in the temporary folder.
        reload(request_key: typing.Hashable) -> typing.Any: Reload the data from the temporary folder.



    """

    def __init__(self, path: str = "./tmp", backend: typing.Any = None):
        """Create a StuffSaver object

        Args:
            path (str, optional): Path to the temporary folder where the data will be saved. Defaults to "./tmp".
            backend (_type_, optional): Backend to use for saving the data. It should have the methods load and dump.
            . Defaults to None which uses the pickle backend.
        """
        mkdir_p(path)
        self.path = path

        if backend is not None:
            self.backend = backend
        else:
            import pickle

            self.backend = pickle

    def exists(self, request_key: typing.Hashable) -> bool:
        """Check if the data exists in the temporary folder.

        Args:
            request_key (typing.Hashable): request_key key to check if the data exists.

        Returns:
            bool: True if the data exists in the temporary folder, False otherwise.
        """

        saving_path = os.path.join(self.path, hasher(request_key))
        return os.path.isfile(saving_path)

    def reload(self, request_key: typing.Hashable) -> typing.Any:
        """
        Reloads the data associated with the given request_key.

        Parameters:
            request_key (typing.Hashable): The request_key to reload the data for.

        Returns:
            typing.Any: The reloaded data.

        Raises:
            FileNotFoundError: If the file associated with the request_key does not exist.
            IOError: If there is an error reading the file.

        """
        saving_path = os.path.join(self.path, hasher(request_key))
        with open(saving_path, "rb") as handle:
            data = self.backend.load(handle)
        return data

    def save(self, request_key: typing.Hashable, data: typing.Any) -> None:
        """
        Save the given data to a file.

        Args:
            request_key (typing.Hashable): The request_key object used to generate the saving path.
            data (typing.Any): The data to be saved.

        Returns:
            None
        """
        saving_path = os.path.join(self.path, hasher(request_key))
        with open(saving_path, "wb") as handle:
            self.backend.dump(data, handle)

    def reload_folder(self) -> typing.List[typing.Any]:
        """
        Reloads the folder specified by `self.path` and returns a list of previously saved data.

        Returns:
            list: A list of loaded data from the files in the folder.
        """
        list_data = []
        for filename in os.listdir(self.path):
            saving_path = os.path.join(self.path, filename)
            with open(saving_path, "rb") as handle:
                data = self.backend.load(handle)
            list_data.append(data)
        return list_data

    def delete(self, request_key: typing.Hashable) -> None:
        """
        Deletes the file associated with the given request_key.
        Args:
            request_key (typing.Hashable): The request_key to delete the file for.
        Returns:
            None
        """

        saving_path = os.path.join(self.path, hasher(request_key))
        if os.path.exists(saving_path):
            os.remove(saving_path)

    def wrap(
        self,
        #
        request_key: typing.Hashable,
        fn: typing.Callable[..., typing.Any],
        *args: typing.Any,
        **kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        """
        Wraps a function call with caching mechanism.
        Args:
            request_key (typing.Hashable): The key used to identify the cached result.
            fn (callable): The function to be wrapped.
            *args: Positional arguments to be passed to the function.
            **kwargs: Keyword arguments to be passed to the function.
        Returns:
            typing.Any: The result of the function call.
        Example:
            >>> def add(a, b):
            ...     return a + b
            ...
            >>> ss = StuffSaver()
            >>> wrapped_add = ss.wrap("add", add, 2, 3)
            >>> print(wrapped_add)
            5
        """

        if self.exists(request_key):
            return self.reload(request_key)
        else:
            result = fn(*args, **kwargs)
            self.save(request_key, result)
            return result


if __name__ == "__main__":
    """
    (base)$  python StuffSaver.py
        Launching the long function (it takes 10s)
        1/10
        2/10
        3/10
        4/10
        5/10
        6/10
        7/10
        8/10
        9/10
        10/10
        The result ( 15 ) was obtained in 0:00:10.028592 seconds.
    (base)$ python StuffSaver.py
        The result ( 15 ) was obtained in 0:00:00.001480 seconds.
    """

    import time
    from datetime import datetime

    def long_function_to_compute(x: int) -> int:
        print("Launching the long function (it takes 10s)")
        for i in range(10):
            time.sleep(1)
            print(str(i + 1) + "/10")
        result = 3 * x
        return result

    a = 5
    ss = StuffSaver()

    # EXAMPLE 1

    request_key = "something i would like to avoid if possible"

    tic = datetime.now()
    if ss.exists(request_key):
        # if already computed before, we reload it from temporary folder
        result = ss.reload(request_key)
    else:
        result = long_function_to_compute(a)
        ss.save(request_key, result)
    toc = datetime.now()
    print("(1) The result (", result, ") was obtained in", toc - tic, "seconds.")

    # EXAMPLE 2

    request_key = "something else i would like to avoid if possible"

    tic = datetime.now()
    result = ss.wrap(request_key, long_function_to_compute, a)
    toc = datetime.now()
    print("(2) The result (", result, ") was obtained in", toc - tic, "seconds.")
