import pandas as pd
import dropbox
import io

def read_csv_file(master_file_directory, master_file):
    api_key = "qBPKlgL-suMAAAAAAAAAAcNGKlPaPcmU0C--wOHxxP1M3q0S0rkmjFUT9DmRYqaA"
    dbx = dropbox.Dropbox(api_key)
    
    _, res = dbx.files_download(f"{master_file_directory}{master_file}")
    return_df = (
        pd.read_csv(res.raw)
        .pipe(lambda x:x.assign(date = pd.to_datetime(x.date)))
    )

    return return_df

def backup_csv_file(master_file_directory, master_file, session_date):
    api_key = "qBPKlgL-suMAAAAAAAAAAcNGKlPaPcmU0C--wOHxxP1M3q0S0rkmjFUT9DmRYqaA"
    dbx = dropbox.Dropbox(api_key)

    try:
        dbx.files_copy(
            f"{master_file_directory}{master_file}",
            f"{master_file_directory}{session_date}/{master_file}",
            autorename=False
        )
    except:
        dbx.files_delete(f"{master_file_directory}{session_date}/{master_file}")

        dbx.files_copy(
            f"{master_file_directory}{master_file}",
            f"{master_file_directory}{session_date}/{master_file}",
            autorename=False
        )

    return 0

def write_csv_file(master_file_directory, master_file, df):
    api_key = "qBPKlgL-suMAAAAAAAAAAcNGKlPaPcmU0C--wOHxxP1M3q0S0rkmjFUT9DmRYqaA"
    dbx = dropbox.Dropbox(api_key)
    
    data = df.to_csv(index=False) # The index parameter is optional

    with io.BytesIO(data.encode()) as stream:
        stream.seek(0)

        dbx.files_upload(
            stream.read(),
            f"{master_file_directory}{master_file}",
            mode=dropbox.files.WriteMode.overwrite)

    return 0