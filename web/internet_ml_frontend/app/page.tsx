import Image from 'next/image'
import Link from 'next/link'

export default function Home() {
    return (
        <main>
            <div className="grid grid-cols-1 place-content-center align-middle gap-y-10 h-screen text-center">
                <div className="grid grid-cols-1 place-self-center">
                    <h1 className="url">
                        <Link href="https://github.com/thamognya/internet-ml">
                            Internet-ML
                        </Link>
                    </h1>
                    <h2 className="url">
                        <Link href="https://links.thamognya.com">
                            by Thamognya Kodi
                        </Link>
                    </h2>
                </div>
                <div className="grid sm:grid-cols-3 grid-cols-1 gap-y-4 place-items-center">
                    <h1 className="url">
                        <Link href="/nlp">NLP</Link>
                    </h1>
                    <h1 className="url">
                        <Link href="/image-gen">
                            Image Generation (in progress)
                        </Link>
                    </h1>
                    <h1 className="url">
                        <Link href="/audio">Audio (in progress)</Link>
                    </h1>
                </div>
            </div>
        </main>
    )
}
