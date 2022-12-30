import './globals.css'
import { Fira_Code } from '@next/font/google'
const fira = Fira_Code({ variable: '--font-fira' })

export default function RootLayout({
    children
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            {/*
        <head /> will contain the components returned by the nearest parent
        head.tsx. Find out more at https://beta.nextjs.org/docs/api-reference/file-conventions/head
      */}
            <head />
            <body className={fira.className}>{children}</body>
        </html>
    )
}
