import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'CertUpload: Securely Store and Share Your Academic Certificates',
  description: 'certupload is an app that allows users to upload their academic result certificates to the cloud. It leverages the Verbwire API to provide a secure and easy way to store and share certificates.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}