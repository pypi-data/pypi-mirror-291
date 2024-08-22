import csv
from datetime import datetime
import aiofiles
import asyncio


class URLTracker:
    """
    Class for tracking URLs and their statuses in a CSV file.

    Attributes
    ----------
    file_path : str
        The path to the CSV file for tracking URLs.

    Methods
    -------
    initialize_csv()
        Initializes the CSV file with headers.
    get_url_status(url: str) -> str
        Gets the status of a URL from the CSV file.
    get_url_stage(url: str) -> str
        Gets the stage of a URL from the CSV file.
    delete_url(url: str)
        Deletes a URL from the CSV file.
    get_all_urls() -> list
        Gets all URLs from the CSV file.
    add_url(url: str, stage: str = 'data_source', status: str = 'pending')
        Adds a URL to the CSV file.
    update_url_status(url: str, stage: str, status: str)
        Updates the status and stage of a URL in the CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the URLTracker with the specified CSV file path.

        Parameters
        ----------
        file_path : str
            The path to the CSV file for tracking URLs.
        """
        self.file_path = file_path

    async def initialize_url_tracker(self):
        """
        Initializes the CSV file with headers.
        """
        async with aiofiles.open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            await writer.writerow(['url', 'stage', 'status', 'last_updated'])

    async def get_url_status(self, url: str) -> str:
        """
        Gets the status of a URL from the CSV file.

        Parameters
        ----------
        url : str
            The URL to get the status for.

        Returns
        -------
        str
            The status of the URL.

        Raises
        ------
        ValueError
            If the URL is not found in the tracking system.
        """
        async with aiofiles.open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            await file.__anext__()  # Skip the header
            for row in reader:
                if row[0] == url:
                    return row[2]
            raise ValueError("URL not found in tracking system")

    async def get_url_stage(self, url: str) -> str:
        """
        Gets the stage of a URL from the CSV file.

        Parameters
        ----------
        url : str
            The URL to get the stage for.

        Returns
        -------
        str
            The stage of the URL.

        Raises
        ------
        ValueError
            If the URL is not found in the tracking system.
        """
        async with aiofiles.open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            await file.__anext__()  # Skip the header
            async for row in reader:
                if row[0] == url:
                    return row[1]
            raise ValueError("URL not found in tracking system")

    async def delete_url(self, url: str):
        """
        Deletes a URL from the CSV file.

        Parameters
        ----------
        url : str
            The URL to delete.

        Raises
        ------
        ValueError
            If the URL is not found in the tracking system.
        """
        rows = []
        url_found = False
        async with aiofiles.open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            header = await file.__anext__()
            async for row in reader:
                if row[0] == url:
                    url_found = True
                else:
                    rows.append(row)
        if not url_found:
            raise ValueError("URL not found in tracking system")

        async with aiofiles.open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            await writer.writerow(header)
            for row in rows:
                await writer.writerow(row)

    async def get_all_urls(self) -> list:
        """
        Gets all URLs from the CSV file.

        Returns
        -------
        list
            A list of all URLs.
        """
        async with aiofiles.open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            await file.__anext__()  # Skip the header
            urls = [row[0] for row in reader]
        return urls

    async def add_url(self, url: str = None, stage: str = 'data_source', status: str = 'pending', urls_list: list = None):
        """
        Add a URL to the file.

        Parameters:
        - url (str): The URL to be added.
        - stage (str): The stage of the URL (default is 'data_source').
        - status (str): The status of the URL (default is 'pending').
        - urls_list (list): List of URLs to be added (default is None).

        Note:
        - If `urls_list` is None, only the single `url` will be added.
        - If `urls_list` is provided, each URL in the list will be added separately.

        Examples:
            # Add single URL
            add_url('https://example.com')

            # Add single URL with custom stage and status
            add_url('https://example.com', stage='processing', status='completed')

            # Add multiple URLs from a list
            urls = [
                'https://example.com',
                'https://example.org',
                'https://example.net'
            ]
            add_url(urls_list=urls)

            # Add multiple URLs from a list with custom stage and status
            urls = [
                'https://example.com',
                'https://example.org',
                'https://example.net'
            ]
            add_url(urls_list=urls, stage='processing', status='completed')

        """
        if urls_list is None:
            async with aiofiles.open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                await writer.writerow([url, stage, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        else:
            async with aiofiles.open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                for url in urls_list:
                    await writer.writerow([url, stage, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    async def update_url_status(self, url: str, stage: str, status: str):
        """
        Updates the status and stage of a URL in the CSV file.

        Parameters
        ----------
        url : str
            The URL to update.
        stage : str
            The new stage of the URL.
        status : str
            The new status of the URL.

        Raises
        ------
        ValueError
            If the URL is not found in the tracking system.
        """
        rows = []
        url_found = False
        async with aiofiles.open(self.file_path, mode='r') as file:
            file_content = await file.read()

        reader = csv.reader(file_content.splitlines())
        header = None
        for row in reader:
            if header is None:
                header = row
                continue
            if row[0] == url:
                row[1] = stage
                row[2] = status
                row[3] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                url_found = True
            rows.append(row)
        if not url_found:
            try:
                await self.add_url(url, stage, status)
            except Exception as e:
                raise Exception(f"Some thing wrong with the URL: {e}")

        async with aiofiles.open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            if header is not None:
                await writer.writerow(header)
            for row in rows:
                await writer.writerow(row)

    async def are_urls_completed(self, stage_name):
        """
        Check if all URLs in a file have completed the specified stage.

        Parameters:
        self (object): The current object.
        stage_name (str): The name of the stage to check for completion.

        Returns:
        bool: True if all URLs have completed the specified stage, False otherwise.
        """
        async with aiofiles.open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            await file.__anext__()  # Skip the header
            async for row in reader:
                url, stage, status, last_updated = row
                if stage == stage_name and status != 'completed':
                    return False
        return True


# Example usage
# if __name__ == '__main__':
#     async def main():
#         CSV_FILE = 'data/over_view/url_tracking.csv'
#         tracker = URLTracker(CSV_FILE)
#         await tracker.initialize_url_tracker()
#         await tracker.add_url('http://example.com')
#         await tracker.update_url_status('http://example.com', 'data_preprocessing', 'in_progress')
#
#     asyncio.run(main())
