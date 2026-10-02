from lib.cuckoo.common.abstracts import Processing


class APISequence(Processing):

    order = 2

    def run(self):
        self.key = "api_sequence"

        api_sequence = []

        behavior = self.results.get("behavior", {})
        processes = behavior.get("processes", [])

        for process in processes:
            pid = process.get("process_id")
            process_name = process.get("process_name", "unknown")

            process_label = f"{pid}:{process_name}"

            for call in process.get("calls", []):
                api = call.get("api")

                if not api:
                    continue

                repeated = call.get("repeated", 0) or 0

                api_sequence.append(
                    f"{process_label} -> {api}"
                )

                for _ in range(int(repeated)):
                    api_sequence.append(
                        f"{process_label} -> {api}"
                    )

        return api_sequence