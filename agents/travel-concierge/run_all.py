import subprocess
import asyncio


async def run_adk_agent():
    process = await asyncio.create_subprocess_shell(
        "adk run travel_concierge",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"ADK agent started with PID: {process.pid}")
    # You can optionally monitor stdout and stderr here
    # stdout, stderr = await process.communicate()
    # if stdout:
    #     print(f"ADK Output:\n{stdout.decode()}")
    # if stderr:
    #     print(f"ADK Errors:\n{stderr.decode()}")
    # await process.wait()
    # print(f"ADK agent finished with exit code: {process.returncode}")


async def run_aztp_integration():
    process = await asyncio.create_subprocess_exec(
        "python", "./aztp_integration.py",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"AZTP integration started with PID: {process.pid}")
    stdout, stderr = await process.communicate()
    if stdout:
        print(f"AZTP Output:\n{stdout.decode()}")
    if stderr:
        print(f"AZTP Errors:\n{stderr.decode()}")
    await process.wait()
    print(f"AZTP integration finished with exit code: {process.returncode}")


async def main():
    # Run both concurrently
    adk_task = asyncio.create_task(run_adk_agent())
    aztp_task = asyncio.create_task(run_aztp_integration())

    await asyncio.gather(adk_task, aztp_task)
    print("Both ADK agent and AZTP integration script execution initiated.")

if __name__ == "__main__":
    asyncio.run(main())
