import uvicorn
import multiprocessing
def main():
    multiprocessing.freeze_support()
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=5,
            # log_config="E:\\Desktop\\backend\\log.ini"
        )
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()
