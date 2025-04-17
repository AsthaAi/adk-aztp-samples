import subprocess
import asyncio


async def run_adk_agent():
    process = await asyncio.create_subprocess_shell(
        "adk run travel_concierge",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"ADK agent started with PID: {process.pid}")

    async def read_stdout():
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            print(f"ADK Output: {line.decode().strip()}")

    async def read_stderr():
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            print(f"ADK Error: {line.decode().strip()}")

    # Start tasks to read stdout and stderr concurrently
    stdout_task = asyncio.create_task(read_stdout())
    stderr_task = asyncio.create_task(read_stderr())

    # Simulate sending input to the ADK agent
    async def send_command(command):
        process.stdin.write(f"{command}\n".encode())
        await process.stdin.drain()  # Ensure the data is sent

    # Wait for the "user:" prompt before sending commands (you might need to adjust the waiting logic)
    await asyncio.sleep(2)  # Give the ADK time to start and show the prompt

    await send_command("somit")
    await asyncio.sleep(1)  # Give time for the ADK to respond

    # Send an exit command to gracefully stop the ADK
    await send_command("exit")

    # Wait for the process to finish and the output/error reading tasks to complete
    await process.wait()
    await stdout_task
    await stderr_task

    print(f"ADK agent finished with exit code: {process.returncode}")


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
